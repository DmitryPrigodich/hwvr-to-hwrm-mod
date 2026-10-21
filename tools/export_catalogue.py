"""Export the remaining demo models using actual renderer/material references."""

import argparse
import gc
import hashlib
import json
import math
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

import UnityPy
from PIL import Image, ImageChops
from UnityPy.classes.PPtr import PPtr
from UnityPy.helpers.MeshHelper import MeshHandler

from build_hod import build
from borrow_native_rig import borrow
from catalogue import ADDITIONAL, native_folder
from export_ship import dae_node, element, rotate, write_dae
from transfer_materials import transfer
from model_size import box, fit


def safe(text):
    return re.sub(r"[^a-z0-9_]+", "_", text.lower()).strip("_")


class Source:
    def __init__(self, data):
        self.env = UnityPy.Environment()
        self.env.path = str(data)
        for path in sorted(data.iterdir()):
            if path.suffix == ".assets" or re.fullmatch(r"level\d+", path.name) or re.fullmatch(r"[0-9a-f]{32}",path.name):
                self.env.load_file(str(path))
        self.objects = list(self.env.objects)
        self.cache = {}
        self.roots = defaultdict(list)
        self.meshes = defaultdict(list)
        self.renderers = defaultdict(list)
        # Prefer reusable resource prefabs over scene instances with world offsets.
        for obj in sorted(self.objects, key=lambda o: (o.assets_file.name != "resources.assets", o.path_id)):
            if obj.type.name == "GameObject":
                self.roots[obj.peek_name() or ""].append(obj)
            elif obj.type.name == "Mesh":
                self.meshes[obj.peek_name() or ""].append(obj)
            elif obj.type.name in ("MeshRenderer", "SkinnedMeshRenderer"):
                d = self.read(obj)
                if obj.type.name == "SkinnedMeshRenderer":
                    mesh = self.resolve(d.get("m_Mesh"), obj.assets_file)
                else:
                    go = self.resolve(d["m_GameObject"], obj.assets_file)
                    components = self.components(go)
                    mf = components.get("MeshFilter")
                    mesh = self.resolve(self.read(mf)["m_Mesh"], mf.assets_file) if mf else None
                if mesh:
                    self.renderers[mesh.peek_name()].append(obj)
        print(f"Indexed {len(self.meshes)} mesh names, {len(self.roots)} object names", flush=True)

    def read(self, obj):
        key = (obj.assets_file.name, obj.path_id)
        if key not in self.cache:
            self.cache[key] = obj.parse_as_dict()
        return self.cache[key]

    def resolve(self, ref, af):
        if not ref or not ref.get("m_PathID"):
            return None
        if ref["m_FileID"] and af.externals[ref["m_FileID"]-1].path.rsplit("/",1)[-1] in ("unity default resources", "unity_builtin_extra"):
            return None
        return PPtr(**ref, assetsfile=af).deref()

    def components(self, go):
        return {o.type.name: o for c in self.read(go)["m_Component"]
                if (o := self.resolve(c["component"], go.assets_file))}

    def parts(self, go, ancestors=(), ignore_root=True):
        cs = self.components(go)
        tr = self.read(cs["Transform"])
        chain = ancestors if ignore_root else (*ancestors, tr)
        renderer = cs.get("MeshRenderer") or cs.get("SkinnedMeshRenderer")
        mesh = None
        if cs.get("MeshFilter"):
            mf = cs["MeshFilter"]
            mesh = self.resolve(self.read(mf)["m_Mesh"], mf.assets_file)
        elif renderer:
            mesh = self.resolve(self.read(renderer).get("m_Mesh"), renderer.assets_file)
        if mesh and renderer:
            yield mesh, renderer, chain
        for ref in tr["m_Children"]:
            child_tr = self.resolve(ref, cs["Transform"].assets_file)
            child_go = self.resolve(self.read(child_tr)["m_GameObject"], child_tr.assets_file)
            yield from self.parts(child_go, chain, False)

    def find_parts(self, spec):
        if self.roots.get(spec["root"]):
            return list(self.parts(self.roots[spec["root"]][0]))
        # Cinematic-only models such as the Radaa carrier have no MESH_ prefab.
        family = spec.get("mesh", spec["root"].replace("MESH_", "SM_"))
        candidates = [(name, items[0]) for name, items in self.meshes.items()
                      if re.fullmatch(re.escape(family)+r"(?:_LOD\d+)?", name)]
        result = []
        for name, mesh in sorted(candidates):
            renderers = self.renderers.get(name, [])
            if not renderers:
                raise ValueError(f"No source renderer/material binding for {name}")
            result.append((mesh, renderers[0], ()))
        return result


def point_transform(vector, chain, normal=False):
    xyz = tuple(vector[:3])
    for tr in reversed(chain):
        xyz = tuple(v/tr["m_LocalScale"][axis] if normal else v*tr["m_LocalScale"][axis]
                    for v, axis in zip(xyz, "xyz"))
        xyz = rotate(xyz, tr["m_LocalRotation"])
        if not normal:
            xyz = tuple(v+tr["m_LocalPosition"][axis] for v, axis in zip(xyz, "xyz"))
    if normal:
        length = math.sqrt(sum(v*v for v in xyz)) or 1
        xyz = tuple(v/length for v in xyz)
    return -xyz[0], xyz[1], xyz[2]


def material_maps(source, obj, folder, prefix):
    material = source.read(obj)
    properties = material["m_SavedProperties"]
    tex = dict(properties.get("m_TexEnvs", []))
    images = {}
    sources = {}
    flags=dict(properties.get('m_Ints',[]));floats=dict(properties.get('m_Floats',[]))
    array_keys={'_MainTex':('_ArrayMainTex','_Enable_Main_Texture_Array'),
                '_NormalMap':('_ArrayNormalMap','_Enable_Normal_Map_Array'),
                '_SurfaceDataTexture':('_ArraySurfaceDataTexture','_Enable_Surface_Data_Texture_Array')}
    for key, suffix in (("_MainTex", "BC"), ("_NormalMap", "N"), ("_SurfaceDataTexture", "MSEE")):
        array_key,array_flag=array_keys[key]
        if flags.get(array_flag,floats.get(array_flag,0)) and tex.get(array_key,{}).get('m_Texture',{}).get('m_PathID'):
            key=array_key
        if key=='_NormalMap' and not tex.get(key,{}).get('m_Texture',{}).get('m_PathID'):
            key='_BumpMap'
        ref = tex.get(key, {}).get("m_Texture")
        texture = source.resolve(ref, obj.assets_file)
        if texture:
            parsed=texture.parse_as_object()
            if texture.type.name=='Texture2DArray':
                index=round(floats.get('_IndexArray',0))
                images[suffix]=parsed.images[index].convert('RGBA')
            else:images[suffix] = parsed.image.convert("RGBA")
            sources[suffix] = dict(name=texture.peek_name(), source=texture.assets_file.name, path_id=texture.path_id)
            if texture.type.name=='Texture2DArray':sources[suffix]['array_slice']=index
    # Some environmental materials use standard Unity property names.
    if "BC" not in images:
        ref = tex.get("_BaseMap", {}).get("m_Texture")
        texture = source.resolve(ref, obj.assets_file)
        if texture:
            images["BC"] = texture.parse_as_object().image.convert("RGBA")
            sources["BC"] = dict(name=texture.peek_name(), source=texture.assets_file.name, path_id=texture.path_id)
    colors = dict(properties.get("m_Colors", []))
    shader = 'ship'
    wireframe = None
    if '_Wireframe' in tex:
        texture=source.resolve(tex['_Wireframe']['m_Texture'],obj.assets_file)
        if texture:
            wireframe=texture.parse_as_object().image.convert('L')
            shader='mattealpha2s'
            line=colors.get('_LineColor',dict(r=.5,g=.9,b=1,a=1))
            images['BC']=Image.new('RGBA',wireframe.size,tuple(round(255*line[c]) for c in 'rgb')+(255,))
            images['BC'].putalpha(wireframe)
            sources['BC']=dict(name=texture.peek_name(),source=texture.assets_file.name,path_id=texture.path_id,
                               conversion='Source wireframe mask and line colour -> transparent diffuse')
    tint = colors.get("_Color", colors.get("_BaseColor", dict(r=1,g=1,b=1,a=1)))
    if "BC" not in images:
        images["BC"] = Image.new("RGBA", (16,16), tuple(round(255*max(0,min(1,tint[c]))) for c in "rgba"))
    size = images["BC"].size
    images.setdefault("N", Image.new("RGBA",size,(128,128,255,255)))
    images.setdefault("MSEE", Image.new("RGBA",size,(0,0,0,0)))
    for suffix, img in images.items():
        if img.size != size:
            img = img.resize(size, Image.Resampling.BILINEAR)
        img.save(folder/f"T_{prefix}_{suffix}.png")
    (folder/"material-source.json").write_text(json.dumps(material,indent=2),encoding="utf-8")
    images["BC"].save(folder/f"vr_{prefix}_DIFF.tga")
    report = transfer(folder, prefix)
    # Standard/URP materials use separate emission and specular/gloss slots.
    emission_ref=tex.get('_EmissionMap',{}).get('m_Texture')
    emission_texture=source.resolve(emission_ref,obj.assets_file)
    if emission_texture:
        emission=emission_texture.parse_as_object().image.convert('RGB').resize(size,Image.Resampling.BILINEAR)
        emission.save(folder/f'vr_{prefix}_GLOW.tga')
        shader='shipglow'
        sources['emission']=dict(name=emission_texture.peek_name(),source=emission_texture.assets_file.name,path_id=emission_texture.path_id)
    gloss_texture=source.resolve(tex.get('_SpecGlossMap',{}).get('m_Texture'),obj.assets_file)
    if gloss_texture:
        gloss=gloss_texture.parse_as_object().image.convert('RGBA').resize(size,Image.Resampling.BILINEAR)
        gloss.getchannel('A').convert('RGB').save(folder/f'vr_{prefix}_SPEC.tga')
        sources['specular_gloss']=dict(name=gloss_texture.peek_name(),source=gloss_texture.assets_file.name,path_id=gloss_texture.path_id)
    if wireframe is not None:
        wireframe.convert('RGB').save(folder/f'vr_{prefix}_GLOW.tga')
    report.update(source_bindings=sources, source_material=material["m_Name"],target_shader=shader)
    (folder/f"vr_{prefix}.material.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    return "vr_"+prefix, tex.get("_MainTex", tex.get("_BaseMap", {})), shader


def write_model(parts, materials, rig, output):
    root = ET.Element("COLLADA", xmlns="http://www.collada.org/2005/11/COLLADASchema",version="1.4.1")
    asset = element(root,"asset");element(asset,"unit",meter=1,name="meter");element(asset,"up_axis","Y_UP")
    images = element(root,"library_images");mats=element(root,"library_materials");effects=element(root,"library_effects")
    geometries=element(root,"library_geometries")
    scene=element(element(root,"library_visual_scenes"),"visual_scene",id="scene")
    material_names={}
    for i,(key,(prefix,shader)) in enumerate(materials.items()):
        name="MAT[Hull"+(str(i) if i else "")+"]_SHD["+shader+"]"
        material_names[key]=name
        image=element(images,"image",id=prefix+"_DIFF",name=prefix+"_DIFF")
        element(image,"init_from",prefix+"_DIFF.tga")
        material=element(mats,"material",id=name,name=name);element(material,"instance_effect",url="#"+name+"-fx")
        effect=element(effects,"effect",id=name+"-fx",name=name+"-fx")
        phong=element(element(element(effect,"profile_COMMON"),"technique",sid="standard"),"phong")
        element(element(phong,"diffuse"),"texture",texture=prefix+"_DIFF",texcoord="CHANNEL0")
    lods={}
    for part in parts:
        lod=part["lod"]
        if lod not in lods:lods[lod]=dae_node(scene,f"ROOT_LOD[{lod}]")
        name=f'MULT[{part["name"]}]_LOD[{lod}]'
        geo=element(geometries,"geometry",id=name,name=name);mesh=element(geo,"mesh")
        for suffix,values,components in (("p",part["positions"],"XYZ"),("n",part["normals"],"XYZ"),("uv",part["uvs"],"ST")):
            sid=name+"-"+suffix;src=element(mesh,"source",id=sid)
            flat=[v for row in values for v in row[:len(components)]]
            element(src,"float_array"," ".join(f"{v:.9g}" for v in flat),id=sid+"-array",count=len(flat))
            acc=element(element(src,"technique_common"),"accessor",source="#"+sid+"-array",count=len(values),stride=len(components))
            for c in components:element(acc,"param",name=c,type="float")
        vertex=element(mesh,"vertices",id=name+"-v");element(vertex,"input",semantic="POSITION",source="#"+name+"-p")
        for key,faces in part["groups"]:
            tri=element(mesh,"triangles",count=len(faces),material=material_names[key])
            for semantic,src,offset in (("VERTEX",name+"-v",0),("TEXCOORD",name+"-uv",1),("NORMAL",name+"-n",2)):
                element(tri,"input",semantic=semantic,source="#"+src,offset=offset,**({"set":0} if semantic=="TEXCOORD" else {}))
            element(tri,"p"," ".join(str(index) for face in faces for index in reversed(face) for _ in range(3)))
        node=dae_node(lods[lod],name);instance=element(node,"instance_geometry",url="#"+name)
        binding=element(element(instance,"bind_material"),"technique_common")
        for key,_ in part["groups"]:
            name_mat=material_names[key]
            bound=element(binding,"instance_material",symbol=name_mat,target="#"+name_mat)
            element(bound,"bind_vertex_input",semantic="CHANNEL0",input_semantic="TEXCOORD",input_set=0)
    # Reuse the tested combat joint and engine shape writer without duplicating it.
    scratch=output.with_name("rig.dae")
    triangle="v 0 0 0\nv 1 0 0\nv 0 1 0\nvt 0 0\nvt 1 0\nvt 0 1\nvn 0 0 1\nvn 0 0 1\nvn 0 0 1\nf 1/1/1 2/2/2 3/3/3\n"
    write_dae([(0,triangle)],next(iter(materials.values()))[0]+"_DIFF.tga",scratch,100,rig)
    ns={"c":"http://www.collada.org/2005/11/COLLADASchema"}
    temp=ET.parse(scratch)
    def unnamespace(node):
        for n in node.iter():n.tag=n.tag.rsplit("}",1)[-1]
        return node
    for node in temp.findall('.//c:visual_scene/c:node',ns):
        if node.get('name')=='ROOT_LOD[0]':
            for child in list(node):
                if child.tag.endswith('node') and child.get('name','').startswith('JNT['):lods[0].append(unnamespace(child))
    for geo in temp.findall('.//c:library_geometries/c:geometry',ns):
        if geo.get('name','').startswith('ETSH['):geometries.append(unnamespace(geo))
    info=dae_node(scene,"ROOT_INFO");element(info,"node",name="Class[MultiMesh]_Version[512]",id="format")
    element(info,"node",name="UVSets[1]",id="uvsets")
    element(element(root,"scene"),"instance_visual_scene",url="#scene")
    ET.indent(root);ET.ElementTree(root).write(output,encoding="utf-8",xml_declaration=True)


def export_one(source, spec, hodor, definitions, views):
    folder=Path("exports/catalogue")/spec["id"];folder.mkdir(parents=True,exist_ok=True)
    raw_parts=source.find_parts(spec)
    if not raw_parts:raise ValueError(f'No geometry for {spec["root"]}')
    parts=[];materials={};reports=[];material_signatures={}
    for mesh_obj,renderer,chain in raw_parts:
        mesh=mesh_obj.parse_as_object();handler=MeshHandler(mesh);handler.process()
        name=mesh.m_Name;match=re.search(r"LOD_?(\d+)",name)
        lod=int(match[1]) if match else 0
        if not handler.m_UV0:raise ValueError(f"No source UVs: {name}")
        rd=source.read(renderer);bindings=rd["m_Materials"]
        groups=[]
        for sub,triangles in enumerate(handler.get_triangles()):
            ref=bindings[min(sub,len(bindings)-1)]
            mat=source.resolve(ref,renderer.assets_file)
            # The cinematic door's distant meshes contain an untextured Lit placeholder.
            # They share the same UV atlas as its LOD0 door renderer.
            if spec['id']=='vr_kus_mothership_door' and mat.peek_name()=='Lit':
                first_renderer=source.renderers['Kus_Mothership_Door_LOD0'][0]
                mat=source.resolve(source.read(first_renderer)['m_Materials'][0],first_renderer.assets_file)
            md=source.read(mat)['m_SavedProperties']
            texprops=dict(md.get('m_TexEnvs',[]));floatprops=dict(md.get('m_Floats',[]));intprops=dict(md.get('m_Ints',[]))
            signature=json.dumps([mat.assets_file.name,
                {k:texprops.get(k) for k in ('_MainTex','_BaseMap','_NormalMap','_SurfaceDataTexture')},
                {k:floatprops.get(k) for k in ('_Smoothness','_Metalness','_EmissionBlue','_EmissionAlpha')},
                {k:intprops.get(k,floatprops.get(k)) for k in ('_Base_Alpha_As_Color_Mask','_TeamColorOn')},
                {k:v for k,v in md.get('m_Colors',[]) if k in ('_Color','_BaseColor')}],sort_keys=True)
            key=material_signatures.setdefault(signature,(mat.assets_file.name,mat.path_id))
            if key not in materials:
                prefix=safe(spec["id"])+"_m"+str(len(materials))
                texture_prefix,texenv,shader=material_maps(source,mat,folder,prefix)
                materials[key]=(texture_prefix,texenv,shader)
            groups.append((key,list(triangles)))
        # All texture slots in these materials use the same UV transform.
        uv_env=materials[groups[0][0]][1]
        uv_scale=uv_env.get("m_Scale",dict(x=1,y=1));uv_offset=uv_env.get("m_Offset",dict(x=0,y=0))
        part={"name":safe(re.sub(r"_?LOD_?\d+", "",name))+"_"+str(sum(p['lod']==lod for p in parts)),"lod":lod,
              "positions":[tuple(v*100 for v in point_transform(p,chain)) for p in handler.m_Vertices],
              "normals":[point_transform(n,chain,True) for n in handler.m_Normals],
              "uvs":[(uv[0]*uv_scale['x']+uv_offset['x'],uv[1]*uv_scale['y']+uv_offset['y']) for uv in handler.m_UV0],"groups":groups}
        parts.append(part);reports.append(dict(mesh=name,lod=lod,source=mesh_obj.assets_file.name,path_id=mesh_obj.path_id,
                                              vertices=len(part['positions']),triangles=sum(len(t) for _,t in groups)))
    # HODOR stops at the first missing LOD index. Some props contain 0,2,3.
    lod_map={lod:index for index,lod in enumerate(sorted({p['lod'] for p in parts}))}
    for part in parts:part['lod']=lod_map[part['lod']]
    raw_bounds=box(p for part in parts if part['lod']==0 for p in part['positions'])
    factor,normalization=fit(spec['id'],raw_bounds)
    for part in parts:part['positions']=[tuple(v*factor for v in p) for p in part['positions']]
    template=""
    if spec.get("archetype"):
        template=(native_folder(spec['archetype'])/(spec['archetype']+'.ship')).read_text(encoding='utf-8-sig')
    weapons=re.findall(r'StartShipWeaponConfig\(NewShipType,"([^"]+)","[^"]*","[^"]*"',template)
    definition=definitions.get(spec.get('definition'),{})
    turrets=[t for t in definition.get('_staticData',{}).get('<Turrets>k__BackingField',[]) if t['InitialTurretState']==0]
    rig={'weapons':[dict(position=list(turrets[i%len(turrets)]['OffsetFromShipCenter'].values()) if turrets else [0,0,0],weapon=w)
                    for i,w in enumerate(weapons)],'engines':[]}
    view=views.get(spec.get('definition'),{})
    for n in view.get('children',[]):
        if any(s in n['name'].lower() for s in ('engine','exhaust','flare')):
            rig['engines'].append(dict(position=list(n['m_LocalPosition'].values()),radius=1))
    for mount in [*rig['weapons'],*rig['engines']]:
        mount['position']=[v*factor for v in mount['position']]
    write_model(parts,{k:(v[0],v[2]) for k,v in materials.items()},rig,folder/'ship.dae')
    build(hodor,folder/'ship.dae',folder/'ship.hod')
    native_rig=None
    if spec.get('archetype'):
        native_rig=borrow(folder/'ship.hod',native_folder(spec['archetype'])/(spec['archetype']+'.hod'))
    lod_bounds={lod:box(p for part in parts if part['lod']==lod for p in part['positions']) for lod in lod_map.values()}
    bounds=box(p for part in parts for p in part['positions'])
    result={**spec,'meshes':reports,'bounds':bounds,'lod_bounds':lod_bounds,'texture_prefixes':[v[0] for v in materials.values()],
            'rig':rig,'weapons':weapons,'scale':100*factor,'normalization':normalization,
            'folder':str(folder),'native_rig':native_rig,'lod_mapping':lod_map}
    (folder/'extraction.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'CATALOGUE_OK {spec["id"]}: {len(parts)} parts, {len(materials)} materials',flush=True)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only', action='append');parser.add_argument('--resume', action='store_true');args=parser.parse_args()
    game=Path(r'C:\Program Files (x86)\Steam\steamapps\common\Homeworld Vast Reaches Demo')
    hodor=Path(r'C:\Program Files (x86)\Steam\steamapps\common\Homeworld 347380\GBXTools\HODOR\HODOR.exe')
    source=Source(game/'HomeworldVastReachesDemo_Data')
    definitions=json.loads(Path('local/recovered/definitions.json').read_text())
    views=json.loads(Path('local/recovered/views.json').read_text())
    specs=list(ADDITIONAL)
    # Add every environmental mesh family and the separate mothership door.
    families=sorted({re.sub(r'_LOD\d+$','',name) for name in source.meshes if
                     name.startswith(('SM_Prop_','SM_Resource_','Kus_Mothership_Door','SM_Shield_Sphere','Vgr_HeavyMissle','SM_ShatterStation_Attack'))
                     and 'InvisibleObstacle' not in name})
    for family in families:
        specs.append(dict(id='vr_'+safe(family),ru=family,root='__raw__',mesh=family,race=None,archetype=None,buildable=False))
    if len({s['id'] for s in specs})!=len(specs):raise ValueError('Catalogue identifier collision')
    report_path=Path('local/catalogue-manifest.json');failure_path=Path('local/catalogue-failures.json')
    results={s['id']:s for s in json.loads(report_path.read_text(encoding='utf-8'))} if report_path.exists() else {}
    failures={s['id']:s for s in json.loads(failure_path.read_text(encoding='utf-8'))} if failure_path.exists() else {}
    for spec in specs:
        if args.only and spec['id'] not in args.only:continue
        try:
            if args.resume and spec['id'] in results and results[spec['id']].get('mesh')==spec.get('mesh'):
                result=results[spec['id']];folder=Path(result['folder'])
                binary=(folder/'ship.hod').read_bytes()
                if b'8888' in binary[binary.find(b'HVMD'):]:
                    build(hodor,folder/'ship.dae',folder/'ship.hod')
                if spec.get('archetype'):
                    result['native_rig']=borrow(folder/'ship.hod',native_folder(spec['archetype'])/(spec['archetype']+'.hod'))
                results[spec['id']]=result
                print(f'CATALOGUE_REUSED {spec["id"]}',flush=True)
            else:
                results[spec['id']]=export_one(source,spec,hodor,definitions,views)
            failures.pop(spec['id'],None)
        except Exception as exc:
            failures[spec['id']]=dict(id=spec['id'],error=str(exc))
            print(f'CATALOGUE_FAILED {spec["id"]}: {exc}',flush=True)
        for path,report in ((report_path,list(results.values())),(failure_path,list(failures.values()))):
            pending=path.with_suffix('.tmp');pending.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');pending.replace(path)
        gc.collect()
    if failures:raise SystemExit(f'{len(failures)} catalogue models need repair')


if __name__=='__main__':main()
