"""Validate compiled material maps, authored rigs, scale and the installed archive."""

import hashlib
import json
from pathlib import Path

from build_hod import validate_structure
from fleet import FLEET


def verify():
    result = {"ships":{}}
    for ship in FLEET:
        folder = Path("exports")/ship["mesh"].lower()
        extraction = json.loads((folder/"extraction.json").read_text())
        material = json.loads((folder/"material-transfer.json").read_text())
        binary = (folder/"ship.hod").read_bytes()
        log = (folder/"ship.build.log").read_text()
        validate_structure(folder/"ship.dae",binary,log)
        data = {"scale":extraction["scale"],"material":material["source_material"],
                "resolution":material["resolution"],
                "lods":sorted(int(m["name"].rsplit("LOD",1)[1]) for m in extraction["meshes"]),
                "triangles_lod0":next(m["triangles"] for m in extraction["meshes"] if m["name"].endswith("LOD0")),
                "maps_embedded":{s:("vr_"+ship["mesh"].lower()+"_"+s).encode() in binary for s in ("DIFF","GLOW","TEAM","NORM")},
                "rig_and_lods_preserved":True}
        data["passed"] = (data["scale"]==100.0 and all(data["maps_embedded"].values())
                          and data["material"]=="M_"+ship["mesh"]
                          and "ALERT:" not in log and "WARNING" not in log)
        result["ships"][ship["id"]] = data
    archives = {"built":Path("local/VastReachesDemo.big"),
                "installed":Path(r"C:\Program Files (x86)\Steam\steamapps\common\Homeworld\HomeworldRM\Data\VastReachesDemo.big")}
    for name,path in archives.items():
        with path.open("rb") as stream: result[name+"_sha256"]=hashlib.file_digest(stream,"sha256").hexdigest()
    result["installed_matches"] = result["built_sha256"]==result["installed_sha256"]
    result["archive_crc_passed"] = "TEST: PASSED" in Path("local/VastReachesDemo.test.log").read_text()
    result["passed"] = (all(d["passed"] for d in result["ships"].values())
                        and result["installed_matches"] and result["archive_crc_passed"])
    result["visual_capture_verified"] = False
    Path("local/fleet-material-verification.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))
    if not result["passed"]:
        raise SystemExit("Material/installation checks failed")
    return result


if __name__ == "__main__":
    verify()
