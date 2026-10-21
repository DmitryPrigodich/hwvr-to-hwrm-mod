"""Compile an exported ship using the installed official Gearbox HODOR."""

import argparse
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from material_identity import namespace_materials


def validate_structure(source, binary, log):
    namespace = {"c": "http://www.collada.org/2005/11/COLLADASchema"}
    for node in ET.parse(source).findall(".//c:node", namespace):
        name = node.get("name", "")
        if name.startswith(("JNT[", "BURN[", "ETSH[")):
            joint = name.split("[", 1)[1].split("]", 1)[0]
            if joint.encode("ascii") not in binary:
                raise RuntimeError(f"HODOR discarded authored rig element: {joint}")
        if name.startswith("ROOT_LOD[") and f"Scene Data LOD[{name.split('[')[1]}" not in log:
            raise RuntimeError(f"HODOR discarded {name}")


def build(hodor: Path, source: Path, output: Path, minimum_size=4096):
    hodor, source, output = hodor.resolve(), source.resolve(), output.resolve()
    shutil.copyfile(hodor.parent / "SHADERS.MAP", source.parent / "SHADERS.MAP")
    pending = output.with_suffix(".pending.hod")
    if pending.exists():
        pending.unlink()
    codec = "ForceDXT5" if "SHD[mattealpha" in source.read_text(encoding="utf-8") else "ForceDXT1"
    result = subprocess.run([str(hodor), "-action=convert",
                             "-$SHADE_OPT_LOADDAE="+codec,
                             f"-$CONVERT_IN={source}", f"-$CONVERT_OUT={pending}"],
                            cwd=source.parent, capture_output=True, text=True)
    log = result.stdout + result.stderr
    output.with_suffix(".build.log").write_text(log, encoding="utf-8")
    print(log)
    # HODOR can return exit code zero even when conversion fails.
    if (result.returncode or "ALERT:" in log or "WARNING" in log
            or not pending.exists() or pending.stat().st_size < minimum_size):
        raise RuntimeError(f"HODOR did not produce a clean model: {output.with_suffix('.build.log')}")
    binary = pending.read_bytes()
    if b"LMIP" not in binary or "Creating STAT[Hull] with Shader[" not in log:
        raise RuntimeError("HOD is missing its embedded hull texture or ship material")
    validate_structure(source, binary, log)
    pending.write_bytes(namespace_materials(binary,source.parent.name))
    pending.replace(output)
    print(f"Built {output}: {output.stat().st_size:,} bytes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hodor", type=Path)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    build(args.hodor, args.source, args.output)
