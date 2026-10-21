"""Extract demo geometry, prefab transforms and combat joints for HODOR."""

import argparse
import hashlib
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import UnityPy


def element(parent, tag, text=None, **attrs):
    child = ET.SubElement(parent, tag, {k: str(v) for k, v in attrs.items()})
    if text is not None:
        child.text = str(text)
    return child


def parse_obj(text):
    positions, normals, uvs, faces = [], [], [], []
    for line in text.splitlines():
        fields = line.split()
        if not fields:
            continue
        if fields[0] in ("v", "vn", "vt"):
            target = {"v": positions, "vn": normals, "vt": uvs}[fields[0]]
            target.append(tuple(map(float, fields[1:])))
        elif fields[0] == "f":
            face = [tuple(int(v) - 1 for v in token.split("/")) for token in fields[1:]]
            if len(face) != 3 or any(len(v) != 3 for v in face):
                raise ValueError("Expected triangulated geometry with UVs and normals")
            faces.append(face)
    return positions, normals, uvs, faces


def rotate(vector, quaternion):
    x, y, z = vector
    qx, qy, qz, qw = (quaternion[k] for k in "xyzw")
    tx, ty, tz = 2 * (qy*z-qz*y), 2 * (qz*x-qx*z), 2 * (qx*y-qy*x)
    return (x+qw*tx+qy*tz-qz*ty, y+qw*ty+qz*tx-qx*tz, z+qw*tz+qx*ty-qy*tx)


def prefab_vertex(vector, transform, normal=False):
    # UnityPy's OBJ exporter mirrors X. Apply the Unity transform in Unity space.
    xyz = (-vector[0], vector[1], vector[2])
    scaling = transform["m_LocalScale"]
    xyz = tuple(v / scaling[k] if normal else v * scaling[k] for v, k in zip(xyz, "xyz"))
    xyz = rotate(xyz, transform["m_LocalRotation"])
    if normal:
        length = math.sqrt(sum(v*v for v in xyz)) or 1
        xyz = tuple(v / length for v in xyz)
    else:
        xyz = tuple(v + transform["m_LocalPosition"][k] for v, k in zip(xyz, "xyz"))
    return -xyz[0], xyz[1], xyz[2]


def dae_node(parent, name, position=(0, 0, 0)):
    node = element(parent, "node", name=name, id=name)
    element(node, "translate", " ".join(f"{v:.9g}" for v in position), sid="translate")
    return node


def write_dae(lods, texture_file, output, scale, rig=None):
    rig = rig or {}
    root = ET.Element("COLLADA", xmlns="http://www.collada.org/2005/11/COLLADASchema",
                      version="1.4.1")
    asset = element(root, "asset")
    element(asset, "unit", meter=1, name="meter")
    element(asset, "up_axis", "Y_UP")
    images = element(root, "library_images")
    texture_id = Path(texture_file).stem
    image = element(images, "image", id=texture_id, name=texture_id)
    element(image, "init_from", texture_file)
    materials = element(root, "library_materials")
    material_name = "MAT[Hull]_SHD[ship]"
    effect_name = material_name + "-fx"
    material = element(materials, "material", id=material_name, name=material_name)
    element(material, "instance_effect", url=f"#{effect_name}")
    effects = element(root, "library_effects")
    effect = element(effects, "effect", id=effect_name, name=effect_name)
    profile = element(effect, "profile_COMMON")
    phong = element(element(profile, "technique", sid="standard"), "phong")
    element(element(phong, "diffuse"), "texture", texture=texture_id, texcoord="CHANNEL0")
    element(element(phong, "specular"), "color", "0.15 0.15 0.15 1")
    geometries = element(root, "library_geometries")
    scene = element(element(root, "library_visual_scenes"), "visual_scene", id="scene")

    for lod, text in lods:
        positions, normals, uvs, faces = parse_obj(text)
        transform = rig.get("lod_transforms", {}).get(str(lod))
        if transform:
            positions = [prefab_vertex(p, transform) for p in positions]
            normals = [prefab_vertex(p, transform, normal=True) for p in normals]
        geometry_id = f"MULT[Hull]_LOD[{lod}]"
        geometry = element(geometries, "geometry", id=geometry_id, name=geometry_id)
        mesh = element(geometry, "mesh")
        for suffix, values, components in (("positions", positions, "XYZ"),
                                             ("normals", normals, "XYZ"),
                                             ("uvs", uvs, "ST")):
            source_id = f"{geometry_id}-{suffix}"
            source = element(mesh, "source", id=source_id)
            factor = scale if suffix == "positions" else 1
            flattened = [v * factor for row in values for v in row[:len(components)]]
            element(source, "float_array", " ".join(f"{v:.9g}" for v in flattened),
                    id=f"{source_id}-array", count=len(flattened))
            accessor = element(element(source, "technique_common"), "accessor",
                               source=f"#{source_id}-array", count=len(values), stride=len(components))
            for component in components:
                element(accessor, "param", name=component, type="float")
        vertices = element(mesh, "vertices", id=f"{geometry_id}-vertices")
        element(vertices, "input", semantic="POSITION", source=f"#{geometry_id}-positions")
        triangles = element(mesh, "triangles", count=len(faces), material=material_name)
        element(triangles, "input", semantic="VERTEX", offset=0, source=f"#{geometry_id}-vertices")
        element(triangles, "input", semantic="TEXCOORD", offset=1, set=0, source=f"#{geometry_id}-uvs")
        element(triangles, "input", semantic="NORMAL", offset=2, source=f"#{geometry_id}-normals")
        element(triangles, "p", " ".join(str(v) for face in faces for vertex in face for v in vertex))
        lod_node = element(scene, "node", name=f"ROOT_LOD[{lod}]", id=f"ROOT_LOD[{lod}]")
        element(lod_node, "translate", "0 0 0", sid="translate")
        hull = element(lod_node, "node", name=geometry_id, id=geometry_id)
        element(hull, "translate", "0 0 0", sid="translate")
        instance = element(hull, "instance_geometry", url=f"#{geometry_id}")
        binding = element(element(instance, "bind_material"), "technique_common")
        bound = element(binding, "instance_material", symbol=material_name, target=f"#{material_name}")
        element(bound, "bind_vertex_input", semantic="CHANNEL0", input_semantic="TEXCOORD", input_set=0)
        if lod == 0:
            for i, point in enumerate(rig.get("weapons", [])):
                position = point["position"]
                position = (-position[0]*scale, position[1]*scale, position[2]*scale)
                prefix = f"Weapon_Gun{i}"
                gun = dae_node(lod_node, f"JNT[{prefix}_Position]", position)
                dae_node(gun, f"JNT[{prefix}_Direction]", (0, 10, 0))
                dae_node(gun, f"JNT[{prefix}_Rest]", (0, 0, 10))
                dae_node(gun, f"JNT[{prefix}_Muzzle]", (0, 0, point.get("muzzle_forward", 0.1)))
            for i, point in enumerate(rig.get("engines", []), 1):
                position = point["position"]
                nozzle = dae_node(lod_node, f"JNT[EngineNozzle{i}]",
                                  (-position[0]*scale, position[1]*scale, position[2]*scale))
                burn = dae_node(nozzle, f"BURN[EngineBurn{i}]")
                for division in range(5):
                    dae_node(burn, f"Flame[0]_Div[{division}]", (0, 0, -division*point["radius"]))
                shape_name = f"ETSH[EngineShape{i}]"
                shape = dae_node(nozzle, shape_name)
                element(shape, "instance_geometry", url=f"#{shape_name}")
                geometry = element(geometries, "geometry", id=shape_name, name=shape_name)
                mesh = element(geometry, "mesh")
                source = element(mesh, "source", id=shape_name+"-positions")
                r = point["radius"]
                element(source, "float_array", f"{-r} {-r} 0 {r} {-r} 0 {r} {r} 0 {-r} {r} 0",
                        id=shape_name+"-array", count=12)
                accessor = element(element(source, "technique_common"), "accessor",
                                   source="#"+shape_name+"-array", count=4, stride=3)
                for component in "XYZ":
                    element(accessor, "param", name=component, type="float")
                vertices = element(mesh, "vertices", id=shape_name+"-vertices")
                element(vertices, "input", semantic="POSITION", source="#"+shape_name+"-positions")
                triangles = element(mesh, "triangles", count=2)
                element(triangles, "input", semantic="VERTEX", source="#"+shape_name+"-vertices", offset=0)
                element(triangles, "p", "0 2 1 0 3 2")
    info = element(scene, "node", id="root-info", name="ROOT_INFO")
    element(info, "node", id="format-info", name="Class[MultiMesh]_Version[512]")
    element(info, "node", id="uv-info", name="UVSets[1]")
    element(element(root, "scene"), "instance_visual_scene", url="#scene")
    ET.indent(root)
    ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)


def export_ship(source: Path, ship: str, output: Path, scale: float, rig=None, extra_sources=()):
    output.mkdir(parents=True, exist_ok=True)
    lods, summary = [], {"source": str(source.resolve()), "ship": ship, "scale": scale,
                         "unitypy": UnityPy.__version__, "meshes": [], "textures": []}
    sources = [source, *extra_sources]
    objects = []
    environments = [UnityPy.load(str(p)) for p in sources]
    for env in environments:
        objects.extend(env.objects)
    for obj in objects:
        if obj.type.name == "Mesh":
            name = obj.peek_name() or ""
            match = re.fullmatch(rf"SM_{re.escape(ship)}_LOD(\d+)", name)
            if not match:
                continue
            text = obj.parse_as_object().export()
            positions, _, _, faces = parse_obj(text)
            (output / f"{name}.obj").write_text(
                "mtllib hull.mtl\nusemtl Hull\n" + text, encoding="utf-8", newline="")
            lods.append((int(match[1]), text))
            summary["meshes"].append({"name": name, "path_id": obj.path_id,
                                       "vertices": len(positions), "triangles": len(faces)})
        elif obj.type.name == "Material" and obj.peek_name() == f"M_{ship}":
            material = obj.parse_as_dict()
            (output/"material-source.json").write_text(json.dumps(material, indent=2), encoding="utf-8")
        elif obj.type.name == "Texture2D":
            name = obj.peek_name() or ""
            if name not in {f"T_{ship}_BC", f"T_{ship}_N", f"T_{ship}_MSEE"}:
                continue
            image = obj.parse_as_object().image
            image.save(output / f"{name}.png")
            summary["textures"].append({"name": name, "path_id": obj.path_id,
                                         "width": image.width, "height": image.height})
            if name.endswith("_BC"):
                image.convert("RGB").save(output / f"vr_{ship.lower()}_DIFF.tga")
    if not lods or not (output / f"vr_{ship.lower()}_DIFF.tga").exists():
        raise ValueError("No complete mesh/base-colour pair found in this serialized file")
    (output / "hull.mtl").write_text(f"newmtl Hull\nKd 1 1 1\nmap_Kd T_{ship}_BC.png\n", encoding="utf-8")
    if len(set(lod for lod, _ in lods)) != len(lods):
        raise ValueError(f"Duplicate LODs for {ship}")
    write_dae(sorted(lods), f"vr_{ship.lower()}_DIFF.tga", output / "ship.dae", scale, rig)
    summary["rig"] = rig
    summary["sources"] = [str(p) for p in sources]
    with source.open("rb") as source_stream:
        summary["source_sha256"] = hashlib.file_digest(source_stream, "sha256").hexdigest()
    (output / "extraction.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Exported {ship}: {len(lods)} LODs, {len(summary['textures'])} textures")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--ship", default="Rad_LanceFighter")
    parser.add_argument("--output", type=Path, default=Path("exports/rad_lancefighter"))
    parser.add_argument("--scale", type=float, default=250.0,
                        help="Provisional Unity mesh -> HWRM units multiplier")
    args = parser.parse_args()
    export_ship(args.source, args.ship, args.output, args.scale)
