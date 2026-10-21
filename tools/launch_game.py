"""Launch HWRM with the installed prototype archive."""

import argparse
import ctypes
import json
import subprocess
from pathlib import Path


def short_path(path):
    buffer = ctypes.create_unicode_buffer(32768)
    if not ctypes.windll.kernel32.GetShortPathNameW(str(path.resolve()), buffer, len(buffer)):
        raise OSError(f"Cannot resolve short path for {path}")
    return buffer.value


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-root", type=Path, default=Path(
        r"C:\Program Files (x86)\Steam\steamapps\common\Homeworld"))
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--scene", action="store_true", help="Open the isolated combat test scene")
    mode.add_argument("--compare", action="store_true", help="Open eight side-by-side VR / native comparison pairs")
    mode.add_argument("--gallery", action="store_true", help="Open the complete model inspection gallery")
    args = parser.parse_args()
    project = Path(__file__).resolve().parent.parent
    executable = args.game_root / "HomeworldRM/Bin/Release/HomeworldRM.exe"
    running = subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                              "@(Get-Process HomeworldRM -ErrorAction SilentlyContinue).Count"],
                             capture_output=True, text=True)
    if running.returncode or running.stdout.strip() != "0":
        raise SystemExit("HomeworldRM is already running. Close the current game before restarting.")
    mod = args.game_root / "HomeworldRM/Data/VastReachesDemo.big"
    if not mod.is_file():
        raise SystemExit("Install local/VastReachesDemo.big in HomeworldRM/Data first")
    command = [str(executable), "-mod", "VastReachesDemo.big",
               "-windowed", "-w", "1280", "-h", "768", "-nomovies", "-locale", "Russian",
               "-luatrace", "-traceHODs", f"-logfilename={project / 'local/HWRM-test.log'}"]
    if args.scene:
        command += ["-dlccampaign", "HW2Campaign.big", "-campaign", "VastReachesTest",
                    "-startinglevel", "Probe"]
    if args.compare:
        command += ["-dlccampaign", "HW2Campaign.big", "-campaign", "VastReachesCompare",
                    "-startinglevel", "Compare"]
    if args.gallery:
        command += ["-dlccampaign", "HW2Campaign.big", "-campaign", "VastReachesGallery",
                    "-startinglevel", "Inspect"]
    print(subprocess.list2cmdline(command), flush=True)
    process = subprocess.Popen(command, cwd=executable.parent)
    (project/"local/last-launched-process.json").write_text(
        json.dumps({"pid": process.pid, "scene": args.scene, "compare": args.compare, "gallery":args.gallery}), encoding="utf-8")
    print(f"HWRM process: {process.pid}")
