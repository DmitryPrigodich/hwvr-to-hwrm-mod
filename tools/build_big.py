"""Package the local prototype with the official Gearbox archive builder."""

import argparse
import subprocess
from pathlib import Path

from launch_game import short_path


def package(archive_tool: Path, root: Path, output: Path):
    root, output = root.resolve(), output.resolve()
    root_short = short_path(root)
    data_files = [p for p in sorted(root.rglob("*")) if p.is_file()
                  and not (p.relative_to(root).parts[:1] == ("locale",)
                           and len(p.relative_to(root).parts) > 2)
                  and "vr_rad_lancefighter" not in p.parts]
    russian = root / "locale/Russian/vastreaches.ucs"
    lines = ['Archive name="Vast Reaches demo prototype"',
             'TOCStart name="VastReachesData" alias="data" relativeroot=""',
             'FileSettingsStart defcompression="2"', 'FileSettingsEnd']
    lines += [root_short + "\\" + str(p.relative_to(root)) for p in data_files]
    lines += ['TOCEnd',
              'TOCStart name="VastReachesLocale" alias="locale" relativeroot="locale\\Russian"',
              'FileSettingsStart defcompression="2"', 'FileSettingsEnd',
              root_short + "\\" + str(russian.relative_to(root)), 'TOCEnd', '']
    manifest = output.with_suffix(".archive.txt")
    manifest.write_text("\r\n".join(lines), encoding="ascii", newline="")
    result = subprocess.run([str(archive_tool.resolve()), "-c", str(manifest),
                             "-r", root_short + "\\", "-a", str(output)], capture_output=True, text=True)
    log = result.stdout + result.stderr
    output.with_suffix(".build.log").write_text(log, encoding="utf-8")
    print(log)
    if (result.returncode or not output.is_file() or output.stat().st_size < 1000000
            or "Error" in log or "Could not" in log):
        raise RuntimeError("Archive creation failed; inspect the build log")
    result = subprocess.run([str(archive_tool.resolve()), "-a", str(output), "-t"],
                            capture_output=True, text=True)
    log = result.stdout + result.stderr
    output.with_suffix(".test.log").write_text(log, encoding="utf-8")
    print(log)
    if result.returncode or "Failed" in log or "ERROR" in log:
        raise RuntimeError("Archive CRC check failed")
    print(f"Packaged {output}: {output.stat().st_size:,} bytes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive_tool", type=Path)
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    package(args.archive_tool, args.root, args.output)
