"""Inventory an installed Unity demo without changing any game files."""

import argparse
import gc
import json
import re
from collections import Counter
from pathlib import Path

import UnityPy


NAMED_TYPES = {
    "GameObject", "Mesh", "Material", "Texture2D", "VideoClip", "AudioClip",
    "TextAsset", "MonoScript", "MonoBehaviour", "AnimationClip",
}


def audit(data_dir: Path, output: Path) -> dict:
    report = {"data_directory": str(data_dir.resolve()), "unitypy": UnityPy.__version__,
              "files": [], "assets": [], "scenes": [], "errors": []}
    totals = Counter()
    sources = sorted(p for p in data_dir.iterdir() if p.is_file() and (
        p.suffix == ".assets" or p.name == "globalgamemanagers"
        or re.fullmatch(r"level\d+", p.name)))
    for source in sources:
        print(f"Reading {source.name}", flush=True)
        env = UnityPy.load(str(source))
        counts = Counter()
        versions = set()
        for obj in env.objects:
            kind = obj.type.name
            counts[kind] += 1
            versions.add(obj.assets_file.unity_version)
            record = {"source": source.name, "path_id": obj.path_id, "type": kind}
            try:
                if kind in NAMED_TYPES:
                    record["name"] = obj.peek_name()
                    if kind == "MonoScript":
                        data = obj.parse_as_object()
                        record.update(class_name=data.m_ClassName,
                                      namespace=data.m_Namespace,
                                      assembly=data.m_AssemblyName)
                    report["assets"].append(record)
                elif kind == "BuildSettings":
                    report["scenes"].append(obj.parse_as_dict())
            except Exception as exc:
                report["errors"].append({**record, "error": str(exc)})
        totals.update(counts)
        report["files"].append({"name": source.name, "bytes": source.stat().st_size,
                                "unity_versions": sorted(versions), "types": dict(counts)})
        del env
        gc.collect()
    report["totals"] = dict(totals.most_common())
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"report": str(output), "totals": report["totals"],
                      "errors": len(report["errors"]), "scenes": report["scenes"]},
                     ensure_ascii=True, indent=2))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_directory", type=Path)
    parser.add_argument("--output", type=Path, default=Path("local/demo-audit.json"))
    args = parser.parse_args()
    audit(args.data_directory, args.output)
