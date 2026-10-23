"""Compose campaign on pinned races/base into a candidate; no install or game launch."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
from layer_runtime import PROJECT,RACES,BASE,configure,check_revision

IDENTITY='VRC-three-layer-candidate-v1'
WORK=PROJECT/'local/mod-layers'
RELEASE=PROJECT/'local/VastReachesLayered-release'


def configure_sdk():
    configure()
    import hwrm_common as common
    return common


def campaign_name(name):
    return name.startswith(('leveldata/campaign/vastreaches','locale/','sound/','ui/speechicons/','ui/mapthumbnails/campaign/vastreaches')) or name=='ui/subtitle.lua'


def attach_research(source):
    from hwrm_inspect import lua_literal
    def literal(value):
        if isinstance(value,list):value={i+1:item for i,item in enumerate(value)}
        if isinstance(value,dict):
            return '{'+','.join('['+lua_literal(key)+']='+literal(item) for key,item in value.items())+'}'
        return lua_literal(value)
    from lupa.lua51 import LuaRuntime
    path=source/'leveldata/campaign/VastReachesMiniCampaign/VRC_Common.lua'
    text=path.read_text(encoding='ascii')
    import re
    text=re.sub(r'^NKR_CampaignUnlocks=[^\n]*\nfunction NKR_GrantCampaignUnlocks\(allowed\).*?^end\n?', '',text,flags=re.M|re.S)
    text=text.replace('    Player_GrantResearchOption(0,"FighterChassis")\n','')
    text=text.replace('        Player_GrantResearchOption(0,"CorvetteChassis")\n','').replace('        Player_GrantResearchOption(0,"HeavyCorvetteUpgrade")\n','')
    unlocks=json.loads((RACES/'design/campaign-unlocks.json').read_text(encoding='utf8'))
    text+='\nNKR_CampaignUnlocks='+literal(unlocks)+'''
function NKR_GrantCampaignUnlocks(allowed)
    for i=1,getn(allowed) do
        local requirements=NKR_CampaignUnlocks[allowed[i]]
        if requirements then
            for j=1,getn(requirements) do
                Player_UnrestrictResearchOption(0,requirements[j])
                Player_GrantResearchOption(0,requirements[j])
                Player_RestrictResearchOption(0,requirements[j])
            end
        end
    end
end
'''
    anchor='for i=1,getn(allowed) do Player_UnrestrictBuildOption(0,allowed[i]) end'
    assert anchor in text
    if '    NKR_GrantCampaignUnlocks(allowed)' not in text:text=text.replace(anchor,anchor+'\n    NKR_GrantCampaignUnlocks(allowed)',1)
    path.write_text(text,encoding='ascii',newline='\n')
    vm=LuaRuntime();vm.execute((source/'scripts/races/kushan/scripts/def_research.lua').read_text(encoding='ascii'))
    research=[row.Name for _,row in vm.globals().research.items()]
    vm.execute((source/'scripts/races/kushan/scripts/def_build.lua').read_text(encoding='ascii'))
    builds=[row.ThingToBuild for _,row in vm.globals().build.items() if row.Type==0]
    data=source/'leveldata/campaign/VastReachesMiniCampaign/VRC_Data.lua'
    data.write_text(data.read_text(encoding='ascii')+'\nVRC_AllResearch='+literal(research)+'\nVRC_AllBuilds='+literal(builds)+'\n',encoding='ascii',newline='\n')


def prepare():
    common=configure_sdk();revision=check_revision()
    subprocess.run([sys.executable,str(RACES/'tools/build.py')],check=True)
    upstream=json.loads((RACES/'local/source.json').read_text(encoding='utf8'))
    source=common.build_directory('vast-reaches',PROJECT)/'source'
    if source.exists():
        assert source.resolve().is_relative_to(common.build_directory('vast-reaches',PROJECT).resolve())
        assert (source/'vrc-layered-id.txt').read_text().strip()==IDENTITY
        shutil.rmtree(source)
    shutil.copytree(Path(upstream['source']),source)
    import build_minicampaign as old_builder
    mini=PROJECT/'minicampaign'
    own={}
    for name,path in common.index(mini).items():
        if not campaign_name(name) or not old_builder.runtime_file(path,mini):continue
        if path.parent.name.lower()=='animatics' and path.name.lower().startswith('vre_'):continue
        target=source/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,target);own[name]=common.sha(path)
    # Race strings come from the race dependency; story strings stay canonical here.
    for language in ('Russian','English'):
        path=source/f'locale/{language}/vrcampaign.ucs'
        rows=path.read_text(encoding='utf16').splitlines()
        rows=[line for line in rows if not line.split('\t',1)[0].isdigit() or not 9960000<=int(line.split('\t',1)[0])<=9960253]
        path.write_text('\n'.join(rows)+'\n',encoding='utf16')
    attach_research(source)
    for path in (source/'leveldata/campaign/VastReachesMiniCampaign').rglob('*.lua'):
        text=path.read_text(encoding='ascii')
        adapted=text.replace('SobGroup_AbilityActivate(','HWMP_SetAbilityAllowed(').replace('SobGroup_SetSpeed(','HWMP_SetSpeedAllowed(')
        if adapted!=text:adapted='dofilepath("data:scripts/hwmp24/effects.lua")\n'+adapted
        path.write_text(adapted,encoding='ascii',newline='\n')
    (source/'vrc-layered-id.txt').write_text(IDENTITY+'\n',encoding='ascii')
    inherited=common.index(Path(upstream['source']));final=common.index(source)
    for name,path in inherited.items():
        if name.startswith(('ship/','weapon/','subsystem/','scripts/races/','scripts/strike groups/','scripts/startingfleets/')) or name=='scripts/familylist.lua':
            assert common.sha(final[name])==common.sha(path),('Campaign shadowed race tuning',name)
    report={'identity':IDENTITY,'source':str(source),'race_commit':revision,'mp_patch_commit':upstream['mp_patch_commit'],
            'fix_revision':upstream['fix_revision'],'campaign_files':sorted(own),'files':{n:common.sha(p) for n,p in final.items()},
            'candidate_only':True,'engine_tested':False,'installed':False,'game_launched':False}
    common.save(WORK/'source.json',report)
    verify();return source


def verify():
    common=configure_sdk()
    report=json.loads((WORK/'source.json').read_text(encoding='utf8'));source=Path(report['source'])
    assert report['files']=={n:common.sha(p) for n,p in common.index(source).items()}
    import verify_campaign_speech
    log=io.StringIO()
    with contextlib.redirect_stdout(log):
        verify_campaign_speech.verify(scripts_only=True,source_override=source,parse_files=set(report['campaign_files'])|{'scripts/hwmp24/effects.lua'})
    (WORK/'campaign-mocks.log').write_text(log.getvalue(),encoding='utf8')
    result={'status':'passed','campaign_speech_and_scenario_mocks':'passed','race_definitions_inherited_unchanged':True,
            'race_commit':report['race_commit'],'mp_patch_commit':report['mp_patch_commit'],'fix_revision':report['fix_revision'],
            'files':len(report['files']),'candidate_only':True,'engine_tested':False,'installed':False}
    common.save(WORK/'verification.json',result);print(json.dumps(result));return result


def package():
    common=configure_sdk();source=prepare()
    import hwrm_archive
    result=hwrm_archive.package_source(source,RELEASE,'VastReachesMiniCampaign.big','Vast Reaches Campaign Demo')
    log_folder=WORK/'package-logs';log_folder.mkdir(parents=True,exist_ok=True)
    for path in RELEASE.iterdir():
        if path.is_file() and path.name.endswith(('.log','.archive.txt')):
            (log_folder/path.name).write_bytes(path.read_bytes());path.unlink()
    for name in ('start_campaign.ps1','Vast Reaches Campaign Demo.cmd'):
        shutil.copy2(PROJECT/name,RELEASE/name)
    movies=PROJECT/'local/campaign-speech/release-movies'
    assert (movies/'vre-movies-id.txt').read_text().strip()=='VRC-rendered-campaign-movies-v1'
    shutil.copytree(movies,RELEASE/'Movies',dirs_exist_ok=True)
    (RELEASE/'README.txt').write_text('Vast Reaches Campaign Demo: isolated three-layer candidate. Not installed or engine-tested. Dependencies are recorded in layers.json.\n',encoding='ascii')
    (RELEASE/'package-id.txt').write_text('VastReachesCampaignDemo-release-v1\n',encoding='ascii')
    shutil.copy2(WORK/'source.json',RELEASE/'layers.json')
    sums={p.relative_to(RELEASE).as_posix():common.sha(p) for p in RELEASE.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt' and '.log' not in p.name and '.archive.txt' not in p.name}
    (RELEASE/'SHA256SUMS.txt').write_text(''.join(v+'  '+k+'\n' for k,v in sorted(sums.items())),encoding='ascii')
    common.save(WORK/'release.json',result);print(json.dumps(result));return result


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--package-candidate',action='store_true');p.add_argument('--verify',action='store_true');args=p.parse_args()
    if args.package_candidate:package()
    elif args.verify:verify()
    else:prepare()
