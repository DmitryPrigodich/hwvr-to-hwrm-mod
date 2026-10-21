"""Read local stock evidence for Novokushan design; never execute game code.

HW1 BIG format references: Relic's released BigFile.c (HomeworldSDL mirror),
https://raw.githubusercontent.com/HomeworldSDL/HomeworldSDL/master/src/Game/BigFile.c
and Lachesis, RBF1.23 specification v0.8, mirrored at
https://gist.github.com/aheadley/aea63fac00e02ce222fd .
The installed Steam archive uses 36-byte TOC records (64-bit timestamp),
not the older specification's 32-byte records. Output stays in the project.
"""
from __future__ import annotations

import hashlib
import json
import re
import struct
from pathlib import Path

from audit_hw2classic_balance import ROOT, tables

ARCHIVE = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Homeworld\Homeworld1Classic\Data\homeworld.big")
TARGET = ROOT / "local/novokushan"


def expand_lzss(data: bytes, expected: int) -> bytes:
    """MSB-first literal/backreference stream, 4K window, EOS at index zero."""
    bitpos = 0

    def bits(count):
        nonlocal bitpos
        value = 0
        for _ in range(count):
            assert bitpos < len(data) * 8, "Truncated compressed entry"
            value = value * 2 + ((data[bitpos // 8] >> (7 - bitpos % 8)) & 1)
            bitpos += 1
        return value

    window, current, output = bytearray(4096), 1, bytearray()
    while True:
        if bits(1):
            values = [bits(8)]
        else:
            index = bits(12)
            if index == 0:
                break
            length = bits(4) + 2
            # Update the window during copying: backreferences may overlap.
            for offset in range(length):
                value = window[(index + offset) % 4096]
                output.append(value)
                window[current] = value
                current = (current + 1) % 4096
            assert len(output) <= expected
            continue
        for value in values:
            output.append(value)
            window[current] = value
            current = (current + 1) % 4096
        assert len(output) <= expected
    assert len(output) == expected, (len(output), expected)
    return bytes(output)


def source_record(path):
    return {"path": path.relative_to(ROOT).as_posix(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    TARGET.mkdir(parents=True, exist_ok=True)
    result = {"engine_tested": False, "method": "Read-only archive/static source inspection",
              "hw1_archive": str(ARCHIVE), "hw1_ships": {}, "local_sources": []}
    wanted = {r"r1\standarddestroyer.shp", r"r1\missiledestroyer.shp"}
    archive_size = ARCHIVE.stat().st_size
    with ARCHIVE.open("rb") as handle:
        assert handle.read(7) == b"RBF1.23"
        count, flags = struct.unpack("<II", handle.read(8))
        assert flags == 1 and count < 100000
        toc = handle.read(count * 36)
        for i in range(count):
            name_length = struct.unpack_from("<H", toc, i * 36 + 8)[0]
            stored, real, start = struct.unpack_from("<III", toc, i * 36 + 12)
            compressed = struct.unpack_from("<I", toc, i * 36 + 32)[0]
            assert name_length < 260 and start + name_length + 1 + stored <= archive_size
            handle.seek(start)
            previous, decoded = 0xD5, bytearray()
            for value in handle.read(name_length):
                previous ^= value
                decoded.append(previous)
            name = decoded.decode("ascii")
            if name.lower() not in wanted:
                continue
            assert handle.read(1) == b"\0"
            data = handle.read(stored)
            if compressed:
                data = expand_lzss(data, real)
            else:
                assert stored == real
            price = int(re.search(rb"(?m)^buildCost\s+(\d+)", data).group(1))
            path = TARGET / "hw1-source" / Path(name.replace("\\", "/"))
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            result["hw1_ships"][name] = dict(source_record(path), buildCost=price,
                archive_offset=start, compressed_size=stored, original_size=real)
    assert set(result["hw1_ships"]) == wanted
    tuning = ROOT / "local/hw2classic/scripts/tuning.lua"
    values, _ = tables(tuning)
    result["classic_research"] = dict(source_record(tuning), ResearchData=values["ResearchData"])
    for relative, pattern in (
        ("local/hwrm-base/scripts/tuning.lua", "ResearchShipExponent"),
        ("local/hw1ships/ship/kus_carrier/kus_carrier.ship", "setConcurrentBuildLimit|CanBuildShips"),
        ("local/hw1ships/ship/kus_mothership/kus_mothership.ship", "setConcurrentBuildLimit|CanBuildShips"),
        ("local/hw1ships/ship/kus_researchship/kus_researchship.ship", "StartShipHardPointConfig"),
        ("local/hw1ships/ship/kus_researchship/kus_researchship.lua", "SobGroup_DockSobGroupAndStayDocked|numberofdockedresearchships = numberofdockedresearchships|Restrict_Kus_Ship\\(playerIndex"),
        ("local/hw1ships/ship/kus_sensorarray/kus_sensorarray.ship", "SensorRange|SensorPing"),
        ("local/hwrm-base/subsystem/hw1_researchmodule/hw1_researchmodule.subs", "isResearch|typeString"),
        ("local/hwrm-base/ui/newui/build/finalbuild.lua", "shipQueueTitle|subsystemQueueTitle"),
        ("local/hwrm-base/scripts/races/hiigaran/scripts/def_build.lua", "^Ship =|^SubSystem ="),
        ("local/hw1ships/ship/kus_interceptor/kus_interceptor.ship", "setSupplyValue"),
        ("local/hwrm-base/scripts/familylist.lua", "^unitcapsFamily"),
        ("local/hwrm-base/scripts/rules/deathmatchhw2/unitcaps/normal.lua", '^supplyLimit\\("(Fighter|Corvette|Capital)"'),
        ("local/hwrm-base/scripts/races/kushan/scripts/research/fighter_tech.lua", "FighterDrive|FighterChassis|RequiredResearch|RequiredSubSystems"),
        ("local/hwrm-base/scripts/races/hiigaran/scripts/research/default.lua", "GraviticAttractionMines|AdvancedResearch & CorvetteProduction"),
        ("local/hw1ships/ship/kus_resourcecontroller/kus_resourcecontroller.ship", "BuildFamily|DockFamily"),
        ("local/hw1ships/ship/tai_researchship/tai_researchship.ship", "StartShipHardPointConfig|addCustomCode"),
        ("local/hw1ships/ship/tai_researchship/tai_researchship.lua", "DockSobGroupAndStayDocked|Restrict_Tai_Ship\\(playerIndex"),
        ("local/hw1ships/ship/tai_researchstation/tai_researchstation.ship", "mainEngineMaxSpeed|thrusterMaxSpeed|maxhealth=|BuildFamily|DockFamily|buildCost|buildTime|HyperSpaceCommand"),
        ("local/hw2ships/ship/hgn_shipyard/hgn_shipyard.ship", 'BuildFamily=|DockFamily=|CanBuildShips'),
    ):
        path = ROOT / relative
        lines = [{"line": i, "text": line} for i, line in enumerate(
            path.read_text(encoding="utf-8-sig").splitlines(), 1) if re.search(pattern, line)]
        assert lines, relative
        result["local_sources"].append(dict(source_record(path), lines=lines))
    station = ROOT / "local/hw1ships/ship/tai_researchstation/tai_researchstation.ship"
    station_text = station.read_text(encoding="utf-8-sig")
    result["stock_tai_station_capabilities"] = {
        "source": source_record(station),
        "CanBuildShips_present": "CanBuildShips" in station_text,
        "StartShipHardPointConfig_present": "StartShipHardPointConfig" in station_text,
        "isResearch_present": "isResearch" in station_text,
        "note": "Absence in stock source; proposed new production is not implemented or engine tested",
    }
    build = ROOT / "local/hwrm-base/scripts/races/hiigaran/scripts/def_build.lua"
    build_text = build.read_text(encoding="utf-8-sig")
    at = build_text.index('"Hgn_Shipyard"')
    begin = build_text.rfind("{", 0, at)
    end = build_text.index("}", at) + 1
    result["stock_shipyard_build_entry"] = dict(source_record(build),
        line=build_text[:begin].count("\n") + 1, text=build_text[begin:end])
    glossary = json.loads((ROOT / "localization/glossary.json").read_text(encoding="utf-8"))
    counterparts = {}
    for entry in glossary:
        if entry.get("scope") != "novokushan" or "native_type" not in entry:
            continue
        source = entry["native_type"]
        ident = source.replace("kus_", "tai_", 1)
        path = ROOT / f"local/hw1ships/ship/{ident}/{ident}.ship"
        counterparts[source] = dict(candidate=ident, exists=path.exists(),
                                   **(source_record(path) if path.exists() else {}))
    assert len(counterparts) == 28
    result["tai_same_name_counterparts"] = counterparts
    for suffix in ("1", "2", "3", "4", "5"):
        ident = "hw1_researchmodule" + suffix
        path = ROOT / f"local/hwrm-base/subsystem/{ident}/{ident}.subs"
        lines = [{"line": i, "text": line} for i, line in enumerate(
            path.read_text(encoding="utf-8-sig").splitlines(), 1) if re.search("isResearch|typeString", line)]
        assert len(lines) == 2 and any(row["text"].endswith("isResearch=1") for row in lines)
        result["local_sources"].append(dict(source_record(path), lines=lines))
    target = TARGET / "mechanics-evidence.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(target), "prices": {
        name: row["buildCost"] for name, row in result["hw1_ships"].items()},
        "ResearchData": values["ResearchData"]}))


if __name__ == "__main__":
    main()
