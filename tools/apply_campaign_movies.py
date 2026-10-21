"""Bind rendered movies to an isolated copy of the current combined mod.

Final WebM files use the stock loose Data/Animatics search path; source audio,
PNG, scripts for rendering and diagnostics are never included in the release.
"""
import hashlib
import json
import re
import shutil
from pathlib import Path

from campaign_cinematic_sources import ROOT
from prepare_intro_sources import save_json

WORK = ROOT/'local/cinematic-update'
SOURCE = WORK/'source'
MOVIES = WORK/'release-movies'
IDENTITY = 'VRC-cinematic-update-source-v1'
MOVIE_IDENTITY = 'VRC-rendered-campaign-movies-v1'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def movie_name(package):
    return 'VRE_'+('Prologue' if package=='prologue' else package.removeprefix('Mission_'))


def wrapper(name,language):
    return '''-- Experimental flat adaptation of the original VR scene; audio is embedded.
MovieScreen = {
    displayName = "$9950146",
    helpTip = "$9950146",
    Layout = {size_WH = {w=1,h=1,wr="scr",hr="scr"}},
    stylesheet = "HW2StyleSheet",
    RootElementSettings = {backgroundColor={0,0,0,255}},
    {
        type="Movie", name="MyMovie",
        filenameV="data:animatics/VastReaches/'''+language+'/'+name+'''.webm",
        Layout = {
            pos_XY={x=0.5,y=0.5,xr="par",yr="par"}, pivot_XY={0.5,0.5},
            lockAspect=1280/720,
            size_WH={w=100000,h=1,wr="px",hr="par"},
            max_WH={w=1,h=1,wr="par",hr="par"},
        },
        fixedAspectRatio=1, greyScale=0, abortFadeOutLength=0.25,
        volumemultiplier=0.88,
    },
}
'''


def add_wrappers(target,index):
    for row in index:
        name=movie_name(row['directory'])
        for language in ('English','Russian'):
            # Locale lookup resolves this descriptor from the selected sibling
            # language BIG, using the native "locale" alias.
            path=target/f'locale/{language}/{name}.lua'
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(wrapper(name,language),encoding='ascii')


def bind_mini(target):
    campaign=target/'leveldata/campaign/VastReachesMiniCampaign.campaign'
    text=campaign.read_text(encoding='ascii')
    text=text.replace('playAnimatic("locale:animatics/VRE_','playAnimatic("locale:VRE_')
    for index,name in ((1,'VRE_Prologue'),(3,'VRE_M4_intro')):
        old=f'Mission[{index}]={{postload=function() end,'
        new=f'Mission[{index}]={{postload=function() playAnimatic("locale:{name}.lua",0,0) end,'
        if old in text:text=text.replace(old,new,1)
        else:assert new in text
    campaign.write_text(text,encoding='ascii')
    chapters=target/'leveldata/campaign/VastReachesMiniCampaign'
    for folder,prefix in (('T01_Training','M01_010_'),('M04_LostDestroyer','M04_010_')):
        path=chapters/folder/(folder+'.lua');text=path.read_text(encoding='ascii')
        # Only remove the existing cinematic quote keys, never the lesson dialogue.
        text=re.sub(r'"'+prefix+r'[^"\n]+",?', '',text)
        path.write_text(text,encoding='ascii')


def bind_full(target,index):
    campaign=target/'leveldata/campaign/VastReachesFull.campaign'
    if not campaign.exists():return
    text=campaign.read_text(encoding='ascii')
    text=text.replace('playAnimatic("locale:animatics/VRE_','playAnimatic("locale:VRE_')
    directories=json.loads((ROOT/'campaign-export/manifests/placements.json').read_text(encoding='utf8'))['missions']
    mission_to_number={row['mission']:i for i,row in enumerate(directories,1)}
    for row in index:
        number=mission_to_number[row['mission']]
        if row['field']=='_introScene':
            old=f'Mission[{number}]={{postload=function() end,'
            new=f'Mission[{number}]={{postload=function() playAnimatic("locale:{movie_name(row["directory"])}.lua",0,0) end,'
            if old in text:text=text.replace(old,new,1)
            else:assert new in text
            chapter=directories[number-1]['directory']
            config=target/f'leveldata/campaign/VastReachesFull/{chapter}/VREX_Setup.lua'
            assert config.exists(),config
            data=config.read_text(encoding='ascii')
            marker='\n-- Opening dialogue is embedded in the postload movie.\nVREX_Config.intro = {}\n'
            if marker not in data:config.write_text(data+marker,encoding='ascii')
        else:
            lines=text.splitlines()
            for i,line in enumerate(lines):
                if line.startswith(f'Mission[{number}]={{'):
                    replacement='postlevel=function(bWin) if bWin==1 then playAnimatic("locale:'+movie_name(row['directory'])+'.lua",1,0) else postLevelComplete() end end'
                    lines[i]=line.replace('postlevel=function() postLevelComplete() end',replacement)
            text='\n'.join(lines)+'\n'
    campaign.write_text(text,encoding='ascii')


def apply():
    WORK.mkdir(parents=True,exist_ok=True)
    base=ROOT/'local/fleet-preview/source'
    original_archive=ROOT/'local/VastReachesMiniCampaign.big'
    installed=json.loads((ROOT/'local/fleet-preview/installation.json').read_text(encoding='utf8'))['archive_sha256']
    baseline=WORK/'baseline'
    expected=json.loads((baseline/'identity.json').read_text(encoding='utf8'))['archive_sha256'] if baseline.exists() else installed
    known={expected}
    if (WORK/'installation.json').exists():known.add(json.loads((WORK/'installation.json').read_text(encoding='utf8'))['archive_sha256'])
    assert installed in known,'Installed release changed outside this cinematic update'
    if not baseline.exists():
        assert sha(original_archive)==expected,'Working archive no longer matches current installed baseline'
        baseline.mkdir()
        shutil.copytree(ROOT/'local/VastReachesCampaignDemo-release',baseline/'release')
        save_json(baseline/'identity.json',{'source':str(base),'archive_sha256':expected,'source_hashes':{p.relative_to(base).as_posix():sha(p) for p in base.rglob('*') if p.is_file()}})
    baseline_data=json.loads((baseline/'identity.json').read_text(encoding='utf8'))
    assert baseline_data['archive_sha256']==expected
    current={p.relative_to(base).as_posix():sha(p) for p in base.rglob('*') if p.is_file()}
    assert current==baseline_data['source_hashes'],'Fleet/research baseline changed during cinematic work'
    marker=SOURCE/'cinematic-update-id.txt'
    if SOURCE.exists():assert marker.read_text().strip()==IDENTITY
    shutil.copytree(base,SOURCE,dirs_exist_ok=True)
    marker.write_text(IDENTITY+'\n',encoding='ascii')
    index=json.loads((ROOT/'campaign-export/cinematics/index.json').read_text(encoding='utf8'))['scenes']
    add_wrappers(SOURCE,index)
    bind_mini(SOURCE)
    # The full campaign remains a preparation artifact, separate from installed missions.
    full=ROOT/'campaign-export/data'
    add_wrappers(full,index)
    bind_full(full,index)
    MOVIES.mkdir(parents=True,exist_ok=True)
    (MOVIES/'vre-movies-id.txt').write_text(MOVIE_IDENTITY+'\n',encoding='ascii')
    files=[]
    for row in index:
        report=json.loads((WORK/'render'/row['directory']/'render.json').read_text(encoding='utf8'))
        for language,short in (('English','en'),('Russian','ru')):
            source=WORK/f'movies/{row["directory"]}.{short}.webm'
            video=next(v for v in report['videos'] if v['language']==short)
            assert sha(source)==video['sha256']
            target=MOVIES/language/(movie_name(row['directory'])+'.webm')
            target.parent.mkdir(exist_ok=True);shutil.copy2(source,target)
            files.append({'path':target.relative_to(MOVIES).as_posix(),'sha256':sha(target),'bytes':target.stat().st_size,'source_package':row['directory'],'language':language})
    changed=[p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob('*') if p.is_file() and p.relative_to(SOURCE).as_posix() in current and sha(p)!=current[p.relative_to(SOURCE).as_posix()]]
    assert set(changed)=={'leveldata/campaign/VastReachesMiniCampaign.campaign','leveldata/campaign/VastReachesMiniCampaign/T01_Training/T01_Training.lua','leveldata/campaign/VastReachesMiniCampaign/M04_LostDestroyer/M04_LostDestroyer.lua'},changed
    report={'status':'prepared_not_installed','release_enabled':False,'source':str(SOURCE),'base_archive_sha256':expected,'changed_existing_files':changed,'new_movie_wrappers':24,'movies':files,'prepared_campaign_hooks':['T1/prologue','M4/intro'],'full_preparation_hooks':12,'fleet_research_files_unchanged':True,'game_launched':False,'engine_tested':False}
    save_json(WORK/'integration.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='movies'},ensure_ascii=False))


if __name__=='__main__':apply()
