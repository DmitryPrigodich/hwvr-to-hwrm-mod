"""Reproducibly extract and compile the current combat roster from installed assets."""

import argparse
import json
from pathlib import Path

from build_hod import build
from export_ship import export_ship
from fleet import FLEET
from transfer_materials import transfer


def build_fleet(game, hodor, only=None):
    data = game / "HomeworldVastReachesDemo_Data"
    audit = json.loads(Path("local/demo-audit.json").read_text(encoding="utf-8"))
    definitions = json.loads(Path("local/recovered/definitions.json").read_text(encoding="utf-8"))
    prefabs = json.loads(Path("local/recovered/prefabs.json").read_text(encoding="utf-8"))
    views = json.loads(Path("local/recovered/views.json").read_text(encoding="utf-8"))
    for ship in FLEET:
        if only and ship["id"] != only:
            continue
        source_names = sorted({a["source"] for a in audit["assets"] if
                              (a["type"] == "Mesh" and (a.get("name") or "").startswith("SM_"+ship["mesh"]+"_LOD"))
                              or (a["type"] == "Texture2D" and a.get("name") in
                                  ["T_"+ship["mesh"]+suffix for suffix in ("_BC", "_N", "_MSEE")])
                              or (a["type"] == "Material" and a.get("name")=="M_"+ship["mesh"])})
        definition = definitions[ship["definition"]]
        turrets = [t for t in definition["_staticData"]["<Turrets>k__BackingField"] if t["InitialTurretState"] == 0]
        if len(turrets) != len(ship["weapons"]):
            raise ValueError(f"Weapon/active turret count mismatch: {ship['id']}")
        rig = {"weapons": [{"position": list(t["OffsetFromShipCenter"].values()), "weapon": w,
                            "muzzle_forward": ship.get("muzzle_forward", 0.1)}
                           for t, w in zip(turrets, ship["weapons"])],
               "engines": [{"position": list(n["m_LocalPosition"].values()), "radius": ship["radius"]}
                           for n in views[ship["definition"]]["children"] if any(
                               s in n["name"].lower() for s in ("engine", "exhaust", "flare"))],
               "lod_transforms": {n["name"].rsplit("LOD", 1)[1]: {
                   k: n[k] for k in ("m_LocalPosition", "m_LocalRotation", "m_LocalScale")}
                                  for n in prefabs[ship["definition"]]["children"] if "_LOD" in n["name"]}}
        if not rig["engines"]:
            raise ValueError(f"No original engine position for {ship['id']}")
        output = Path("exports") / ship["mesh"].lower()
        export_ship(data/source_names[0], ship["mesh"], output, ship["scale"], rig,
                    [data/n for n in source_names[1:]])
        if ship.get("full_materials"):
            transfer(output,ship["mesh"])
        build(hodor, output/"ship.dae", output/"ship.hod")
        if ship.get("full_materials"):
            binary = (output/"ship.hod").read_bytes()
            for suffix in ("DIFF","GLOW","TEAM","NORM"):
                if ("vr_"+ship["mesh"].lower()+"_"+suffix).encode() not in binary:
                    raise RuntimeError(f"Missing compiled {suffix} material map: {ship['id']}")
        print(f"FLEET_OK {ship['id']}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("game", type=Path)
    parser.add_argument("hodor", type=Path)
    parser.add_argument("--only", choices=[s["id"] for s in FLEET])
    args = parser.parse_args()
    build_fleet(args.game, args.hodor, args.only)
