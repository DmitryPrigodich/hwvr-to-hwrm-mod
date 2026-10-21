"""Build eight stationary VR/native pairs with camera shortcuts 1-8."""

import json
from pathlib import Path

from export_ship import parse_obj, prefab_vertex
from fleet import FLEET


# Match the visible hull, independently of the current combat archetype.
NATIVE_HULLS = [
    "kus_scout", "kus_interceptor", "kus_attackbomber", "kus_ioncannonfrigate",
    "vgr_interceptor", "vgr_bomber", "vgr_lancefighter", "vgr_lasercorvette",
]
KEYS = ["ONEKEY", "TWOKEY", "THREEKEY", "FOURKEY", "FIVEKEY", "SIXKEY", "SEVENKEY", "EIGHTKEY"]


def prepare():
    project = Path(__file__).resolve().parent.parent
    folder = project / "mod/leveldata/campaign/VastReachesCompare/Compare"
    level = ["function DetermChunk()"]
    pairs = []
    for i, (ship, native) in enumerate(zip(FLEET, NATIVE_HULLS), 1):
        export = project / "exports" / ship["mesh"].lower()
        info = json.loads((export / "extraction.json").read_text())
        points = parse_obj((export / f'SM_{ship["mesh"]}_LOD0.obj').read_text())[0]
        points = [tuple(v * info["scale"] for v in prefab_vertex(p, info["rig"]["lod_transforms"]["0"]))
                  for p in points]
        dimensions = [max(p[axis] for p in points) - min(p[axis] for p in points) for axis in range(3)]
        size = max(20, *dimensions)
        gap = max(15, dimensions[0] * 0.8, size * 0.45)
        center = (i-1) * 700
        for side, kind, x in (("VR", ship["id"], center-gap), ("RM", native, center+gap)):
            group = f"Compare_{i}_{side}"
            level += [f'    addSquadron("{group}", "{kind}", {{{x:.3f}, 0, 0}}, 0, {{0, 0, 0}}, 1, 0)',
                      f'    createSOBGroup("{group}")', f'    addToSOBGroup("{group}", "{group}")']
        level += [f'    addCamera("Compare_Camera{i}", {{{center}, 0, {size*0.15:.3f}}}, '
                  f'{{{center}, {size*1.15:.3f}, {size*2.05:.3f}}})']
        pairs.append({"index": i, "vr": ship["id"], "rm": native, "title_ru": ship["ru"],
                      "subtitle": 9901100+i, "dimensions": dimensions})
    level += ['    setWorldBoundsInner({2450, 0, 0}, {6500, 6000, 6000})', 'end',
              'function NonDetermChunk()', '    loadBackground("m01")',
              '    setSensorsManagerCameraDistances(15, 12000)', 'end',
              'levelDesc = "Eight VR / Remastered comparison pairs"', 'maxPlayers = 2', 'player = {}',
              'player[0] = {id=0, name="", resources=0, raceName="Novokushan", startPos=0}',
              'player[1] = {id=1, name="", resources=0, raceName="Radaa", startPos=0}']
    (folder / "Compare.level").write_text("\n".join(level)+"\n", encoding="utf-8")
    lua = ['dofilepath("data:scripts/SCAR/SCAR_Util.lua")', 'Compare_Current = 1',
           'function OnInit()', '    print("VR_COMPARE8: init")',
           '    Rule_AddInterval("Compare_Ready", 1)', 'end', 'function Compare_Ready()']
    for pair, key in zip(pairs, KEYS):
        i = pair["index"]
        lua += [f'    SobGroup_AbilityActivate("Compare_{i}_VR", AB_Attack, 0)',
                f'    SobGroup_AbilityActivate("Compare_{i}_RM", AB_Attack, 0)',
                f'    print("VR_COMPARE8: pair={i} vr={pair["vr"]} count="..SobGroup_Count("Compare_{i}_VR")..'
                f'" rm={pair["rm"]} count="..SobGroup_Count("Compare_{i}_RM"))',
                f'    UI_BindKeyEvent({key}, "Compare_View{i}")']
    lua += ['    print("VR_COMPARE8: ready pairs=8 keys=1-8")', '    Compare_Show(1)',
            '    Rule_Remove("Compare_Ready")', 'end',
            'function Compare_Show(index)', '    Compare_Current = index',
            '    Camera_Interpolate("here", "Compare_Camera"..index, 0)',
            '    Subtitle_Message("$"..(9901100+index), 900)',
            '    print("VR_COMPARE8: view="..index)', 'end']
    for i in range(1, 9):
        lua += [f'function Compare_View{i}()', f'    Compare_Show({i})', 'end']
    (folder / "Compare.lua").write_text("\n".join(lua)+"\n", encoding="utf-8")
    (project / "local/comparison-pairs.json").write_text(json.dumps(pairs, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Prepared 8 VR/native comparison pairs, camera keys 1-8")


if __name__ == "__main__":
    prepare()
