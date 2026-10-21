"""Generate isolated live-engine weapon tests, one target per imported ship type."""

from pathlib import Path

from fleet import FLEET
from source_weapon_mounts import WEAPONS

IMPORTED_TEST_SHIPS = FLEET + [dict(id=identifier) for identifier,weapons in WEAPONS.items() if weapons]+[dict(id='rad_missilecorvette')]
PROBE_SHIPS = IMPORTED_TEST_SHIPS + [dict(id="native_ion_control", spawn="hgn_ioncannonfrigate")]

def prepare():
    folder = Path("mod/leveldata/campaign/VastReachesTest/Probe")
    level = ['function DetermChunk()']
    for i, ship in enumerate(PROBE_SHIPS, 1):
        x = (i-1)*6000
        distance = 1800
        for name, kind, z, player in ((f"VR_Attacker{i}", ship.get("spawn", ship["id"]), 0, 0),
                                       (f"VR_Target{i}", "vr_combat_target", distance, 1)):
            level += [f'addSquadron("{name}","{kind}",{{{x},0,{z}}},{player},{{0,0,0}},1,0)',
                      f'createSOBGroup("{name}")', f'addToSOBGroup("{name}","{name}")']
        # A real spotter supplies combat visibility independently of FOW UI reveal.
        level += [f'addSquadron("VR_Spotter{i}","hgn_probe",{{{x},500,{distance}}},0,{{0,0,0}},1,0)']
    level += ['addCamera("VR_TestCamera",{0,0,0},{300,160,-380})',
              'setWorldBoundsInner({24000,0,0},{60000,8000,8000})', 'end',
              'function NonDetermChunk()', 'loadBackground("m01")',
              'setSensorsManagerCameraDistances(100,100000)', 'end',
              'levelDesc="Vast Reaches combat probe"', 'maxPlayers=2', 'player={}',
              'player[0]={id=0,name="",resources=20000,raceName="Novokushan",startPos=0}',
              'player[1]={id=1,name="",resources=0,raceName="Radaa",startPos=0}']
    (folder/"Probe.level").write_text("\n".join(level)+"\n", encoding="utf-8")
    script = ['dofilepath("data:scripts/SCAR/SCAR_Util.lua")', 'VR_Ticks=0', 'function OnInit()', 'print("VR_COMBAT: init")',
              'Rule_AddInterval("VR_Start",2)', 'end', 'function VR_Start()']
    for i, ship in enumerate(PROBE_SHIPS, 1):
        script += [f'FOW_RevealGroup("VR_Target{i}",1)',
                   f'SobGroup_AbilityActivate("VR_Target{i}",AB_Attack,0)',
                   f'SobGroup_Attack(0,"VR_Attacker{i}","VR_Target{i}")',
                   f'print("VR_COMBAT: loaded {ship["id"]} count="..SobGroup_Count("VR_Attacker{i}"))']
    script += ['Camera_Interpolate("here","VR_TestCamera",0)',
               f'Subtitle_Message("Vast Reaches: combat test, {len(IMPORTED_TEST_SHIPS)} ship types",12)',
               'Rule_AddInterval("VR_Sample",5)', 'Rule_Remove("VR_Start")', 'end',
               'function VR_Sample()', 'VR_Ticks=VR_Ticks+1']
    for i, ship in enumerate(PROBE_SHIPS, 1):
        script += [f'local pos=SobGroup_GetPosition("VR_Attacker{i}")',
                   f'print("VR_COMBAT: sample="..VR_Ticks.." ship={ship["id"]} target="..SobGroup_HealthPercentage("VR_Target{i}").." attacker="..SobGroup_HealthPercentage("VR_Attacker{i}").." z="..pos[3].." attack="..SobGroup_IsDoingAbility("VR_Attacker{i}",AB_Attack))']
    script += ['if VR_Ticks>=20 then', 'print("VR_COMBAT: complete")',
               'Rule_Remove("VR_Sample")', 'end', 'end']
    (folder/"Probe.lua").write_text("\n".join(script)+"\n", encoding="utf-8")
    print(f"Prepared live combat probe for {len(IMPORTED_TEST_SHIPS)} imported types")


if __name__ == "__main__":
    prepare()
