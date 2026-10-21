"""Check movies and Lua 5.1 hook semantics without HWRM.

This is not a native Lua 4 parser. MovieScreen uses explicit [1] record fields
to avoid Lua 4's different separator grammar for mixed record/list tables.
"""
import concurrent.futures
import hashlib
import json
import re
import subprocess
from pathlib import Path

from lupa.lua51 import LuaRuntime
from apply_campaign_movies import WORK,SOURCE,MOVIES,ROOT,movie_name,sha
from render_campaign_movies import FFMPEG
from prepare_intro_sources import save_json


def video_check(row):
    path=MOVIES/row['path']
    assert sha(path)==row['sha256']
    header=subprocess.run([str(FFMPEG),'-hide_banner','-i',str(path)],capture_output=True,text=True).stderr
    assert re.search(r'Video: vp8, yuv420p.*1280x720.*30 fps',header),header
    assert re.search(r'Audio: vorbis, 44100 Hz, stereo',header),header
    package=row['source_package']
    report=json.loads((WORK/'render'/package/'render.json').read_text(encoding='utf8'))
    match=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',header)
    duration=int(match[1])*3600+int(match[2])*60+float(match[3])
    assert abs(duration-report['duration_seconds'])<.15,(path,duration)
    # Decode the complete file, checking video/audio errors and audible levels.
    result=subprocess.run([str(FFMPEG),'-hide_banner','-nostats','-threads','1','-i',str(path),'-af','volumedetect','-f','null','-'],capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    assert not any(s in result.stderr.lower() for s in ('invalid data','error while decoding','corrupt frame'))
    mean=float(re.search(r'mean_volume: ([-\d.]+) dB',result.stderr)[1])
    maximum=float(re.search(r'max_volume: ([-\d.]+) dB',result.stderr)[1])
    assert -60<mean<-5 and maximum<=0,(path,mean,maximum)
    return {'file':row['path'],'duration':duration,'video':'VP8/yuv420p/1280x720/30fps','audio':'Vorbis/stereo/44100Hz','mean_db':mean,'max_db':maximum,'full_decode':'passed'}


def verify(scripts_only=False):
    integration=json.loads((WORK/'integration.json').read_text(encoding='utf8'))
    if scripts_only:
        videos=[]
        for row in integration['movies']:
            assert sha(MOVIES/row['path'])==row['sha256']
            videos.append({'file':row['path'],'sha256':row['sha256'],'unchanged_video':'hash_verified'})
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            videos=list(pool.map(video_check,integration['movies']))
    index=json.loads((ROOT/'campaign-export/cinematics/index.json').read_text(encoding='utf8'))['scenes']
    assert len(videos)==24
    for target in (SOURCE,ROOT/'campaign-export/data'):
        for row in index:
            name=movie_name(row['directory'])
            for language in ('Russian','English'):
                path=target/f'locale/{language}/{name}.lua'
                vm=LuaRuntime();vm.execute(path.read_text(encoding='ascii'))
                filename=vm.globals().MovieScreen[1].filenameV
                assert filename==f'data:animatics/VastReaches/{language}/{name}.webm'
                assert (MOVIES/language/(name+'.webm')).is_file()
    hooks=[]
    for target,campaign,expected in ((SOURCE,'VastReachesMiniCampaign',{1:'VRE_Prologue',3:'VRE_M4_intro'}),(ROOT/'campaign-export/data','VastReachesFull',{i:movie_name(row['directory']) for i,row in enumerate(index[:-1],1)})):
        vm=LuaRuntime(unpack_returned_tuples=True);calls=[]
        vm.globals().playAnimatic=lambda *args:calls.append(args)
        vm.globals().postLevelComplete=lambda:calls.append(('complete',))
        vm.execute((target/f'leveldata/campaign/{campaign}.campaign').read_text(encoding='ascii'))
        # Full campaign has an additional M1 chapter after the shared T1 prologue.
        if campaign=='VastReachesFull':expected={1:'VRE_Prologue',**{i+3:movie_name(row['directory']) for i,row in enumerate(index[1:-1])}}
        for number,name in expected.items():
            calls.clear();vm.globals().Mission[number].postload()
            assert calls==[(f'locale:{name}.lua',0,0)],(campaign,number,calls)
            hooks.append((campaign,number,name))
        calls.clear();vm.globals().Mission[2].postload();assert not calls,'M1 must not repeat prologue'
        if campaign=='VastReachesFull':
            calls.clear();vm.globals().Mission[12].postlevel(0);assert calls==[('complete',)]
            calls.clear();vm.globals().Mission[12].postlevel(1);assert calls==[('locale:VRE_M13_outro.lua',1,0)]
            for config in (target/'leveldata/campaign/VastReachesFull').glob('*/VREX_Setup.lua'):
                data=config.read_text(encoding='ascii')
                if config.parent.name!='M01_ProvingGrounds':assert data.endswith('VREX_Config.intro = {}\n'),config
    for chapter,prefix in (('T01_Training','M01_010_'),('M04_LostDestroyer','M04_010_')):
        path=SOURCE/f'leveldata/campaign/VastReachesMiniCampaign/{chapter}/{chapter}.lua'
        assert prefix not in path.read_text(encoding='ascii')
    # All prior fleet, research, weapon and localization files remain identical.
    original=json.loads((WORK/'baseline/identity.json').read_text(encoding='utf8'))['source_hashes']
    changes=[name for name,value in original.items() if sha(SOURCE/name)!=value]
    assert set(changes)==set(integration['changed_existing_files']) and len(changes)==3
    import verify_minicampaign as mini
    mini.ROOT=SOURCE;mini.BASE=SOURCE/'leveldata/campaign/VastReachesMiniCampaign';mini.tests()
    # Parse installer and launchers without running them.
    installer=ROOT/'install_minicampaign.ps1'
    command="$tokens=$null; $errors=$null; [System.Management.Automation.Language.Parser]::ParseFile('"+str(installer).replace("'","''")+"',[ref]$tokens,[ref]$errors) | Out-Null; if ($errors.Count) { $errors | Out-String | Write-Error }"
    parsed=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
    assert parsed.returncode==0,parsed.stderr
    assert '-nomovies' not in (ROOT/'start_campaign.ps1').read_text(encoding='utf8')
    report={'status':'passed','videos':videos,'postload_hooks':hooks,'no_duplicate_intro_lines':True,'full_final_success_only':True,'baseline_files_unchanged_except_three_campaign_files':True,'campaign_mock_regression':'passed','powershell_parse':'passed','engine_tested':False,'game_launched':False}
    report['video_decode_repeated']=not scripts_only
    save_json(WORK/('verification-scripts.json' if scripts_only else 'verification.json'),report)
    print(json.dumps({'status':'passed','videos_fully_decoded':0 if scripts_only else len(videos),'video_hashes_verified':len(videos),'postload_hooks':len(hooks),'engine_tested':False}))


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--scripts-only',action='store_true')
    verify(scripts_only=parser.parse_args().scripts_only)
