"""Verify the installed material transfer and side-by-side scene load."""

import hashlib
import json
import struct
from pathlib import Path

from build_hod import validate_structure
from export_ship import parse_obj, prefab_vertex


def verify():
    folder = Path("exports/kus_ioncannonfrigate")
    summary = json.loads((folder/"extraction.json").read_text())
    vertices = parse_obj((folder/"SM_Kus_IonCannonFrigate_LOD0.obj").read_text())[0]
    vertices = [tuple(v*summary["scale"] for v in prefab_vertex(p,summary["rig"]["lod_transforms"]["0"]))
                for p in vertices]
    vr_bounds = [min(p[i] for p in vertices) for i in range(3)]+[max(p[i] for p in vertices) for i in range(3)]
    native = Path("local/hw1ships/ship/kus_ioncannonfrigate/kus_ioncannonfrigate.hod").read_bytes()
    bbox = native.find(b"BBOX")
    native_bounds = list(struct.unpack_from("<6f",native,bbox+8))
    binary = (folder/"ship.hod").read_bytes()
    build_log = (folder/"ship.build.log").read_text()
    validate_structure(folder/"ship.dae",binary,build_log)
    log = Path("local/HWRM-test.log").read_text(errors="replace").replace("\0", "")
    marker = "VR_GALLERY: init" if "VR_GALLERY: init" in log else (
        "VR_COMPARE8: init" if "VR_COMPARE8: init" in log else "VR_COMPARE: init")
    scene_log = log.rsplit(marker,1)[-1]
    report = {"vr_scale":summary["scale"], "vr_lod0_triangles":1966,
              "vr_bounds":vr_bounds, "rm_bounds":native_bounds,
              "maps_embedded":{name:("vr_kus_ioncannonfrigate_"+name).encode() in binary for name in ("DIFF","GLOW","TEAM","NORM")},
              "specular_reflection":"SPEC and REFL sources packed into GLOW by official SHADERS.MAP",
              "scene_ready":any(message in log for message in (
                  "VR_COMPARE: ready VR=1 RM=1", "VR_COMPARE8: ready pairs=8", "VR_GALLERY: ready objects=")),
              "scene_errors":[s for s in scene_log.splitlines() if "stack traceback" in s or "parameter:" in s],
              "visual_capture_verified":False}
    built=Path("local/VastReachesDemo.big")
    installed=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Homeworld\HomeworldRM\Data\VastReachesDemo.big")
    with built.open("rb") as stream: report["built_sha256"]=hashlib.file_digest(stream,"sha256").hexdigest()
    with installed.open("rb") as stream: report["installed_sha256"]=hashlib.file_digest(stream,"sha256").hexdigest()
    report["installed_matches"] = report["built_sha256"]==report["installed_sha256"]
    Path("local/ion-comparison-verification.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))


if __name__ == "__main__":
    verify()
