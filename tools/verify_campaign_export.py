"""Validate prepared text, assets and map wiring without launching the game."""
import collections
import hashlib
import json
import math
import re
import wave
from pathlib import Path

from lupa.lua51 import LuaRuntime
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'campaign-export'
DATA=OUT/'data'


def main():
    read=lambda p:json.loads(p.read_text(encoding='utf8'))
    text=read(OUT/'manifests/localization.json')
    assert len(text)==601
    ids={str(v['id']) for v in text.values()};assert len(ids)==len(text)
    for lang in ['English','Russian']:
        rows=(DATA/f'locale/{lang}/vre_campaign.ucs').read_text(encoding='utf-16').splitlines()
        assert {r.split('\t',1)[0] for r in rows}==ids
    lua_count=0
    for p in DATA.rglob('*'):
        if p.suffix not in ('.lua','.level','.campaign'):continue
        source=p.read_text(encoding='ascii');LuaRuntime().execute('assert(loadstring(...))',source)
        for target in re.findall(r'dofilepath\("data:([^\"]+)"\)',source):
            assert (DATA/target).is_file() or (ROOT/'local/hwrm-base'/target).is_file(),(p,target)
        for ident in re.findall(r'"\$(996\d+)"',source):assert ident in ids,(p,ident)
        lua_count+=1
    manifest=read(OUT/'manifests/placements.json')
    expected=['Mission_T1','Mission_M1','Mission_M7','Mission_M3','Mission_M4','Mission_M5','Mission_M6','Mission_M9','Mission_M10','Mission_M11','Mission_M8','Mission_M13']
    assert manifest['mission_order']==expected
    campaign=LuaRuntime();campaign.execute((DATA/'leveldata/campaign/VastReachesFull.campaign').read_text())
    assert [campaign.globals().Mission[i].directory for i in range(1,13)]==[m['directory'] for m in manifest['missions']]
    maps=[]
    for chapter in manifest['missions']:
        runtime=LuaRuntime(unpack_returned_tuples=True);g=runtime.globals();units={};groups={};volumes={};points=[]
        def create(name):assert name not in groups,name;groups[name]=set()
        def add(name,hull,position,owner,rotation,arg6,delayed):
            assert name not in units,name
            assert owner in range(4)
            assert any((ROOT/path/'ship'/hull/(hull+'.ship')).is_file() for path in ['local/hw1ships','local/hw2ships','local/hwrm-base']),hull
            pos=list(position.values());assert all(math.isfinite(x) for x in pos)
            units[name]={'hull':hull,'owner':owner,'position':pos,'delayed':delayed};points.append(pos)
        def group(name,collective):assert name in units and collective in groups,(name,collective);groups[collective].add(name)
        def sphere(name,position,radius):assert name not in volumes;volumes[name]=(list(position.values()),radius)
        def asteroid(name,position,*args):points.append(list(position.values()))
        noop=lambda *args:None
        for name,fn in {'createSOBGroup':create,'addSquadron':add,'addToSOBGroup':group,'addSphere':sphere,'addAsteroid':asteroid,'addCamera':noop,'setWorldBoundsInner':noop,'loadBackground':noop,'setSensorsManagerCameraDistances':noop}.items():g[name]=fn
        directory=DATA/'leveldata/campaign/VastReachesFull'/chapter['directory']
        runtime.execute((directory/(chapter['directory']+'.level')).read_text());g.DetermChunk();g.NonDetermChunk()
        assert len(units)==sum(len(group['units']) for group in chapter['groups'])
        for source in chapter['groups']:
            assert source['sob'] in groups
            assert groups[source['sob']]=={u['name'] for u in source['units']},source['key']
            for u in source['units']:
                actual=units[u['name']]
                assert actual['delayed']==(0 if source['initial'] else 1),(chapter['mission'],u['name'])
                assert actual['owner']==source['owner']
                assert u['volume'] in volumes
        maps.append({'chapter':chapter['directory'],'explicit_native_requests':len(units),'initial_requests':sum(u['delayed']==0 for u in units.values()),'deferred_requests':sum(u['delayed']==1 for u in units.values()),'group_wiring_checked':True})
    portraits=read(OUT/'manifests/characters.json');loading=read(OUT/'manifests/loading.json');dialogue=read(OUT/'manifests/dialogue.json')
    for image in OUT.glob('assets/**/*.png'):
        with Image.open(image) as f:f.load();assert f.width>0 and f.height>0
    for chapter in loading:
        with Image.open(OUT/chapter['hwrm_loading_dds']) as f:assert f.format=='DDS';f.load()
        assert (OUT/chapter['hwrm_loading_dds']).read_bytes()[84:88]==b'DXT1'
    for c in portraits:
        assert re.search('[А-Яа-я]',c['ru']),c['name_key']
        if c.get('hwrm_portrait_candidate'):
            with Image.open(OUT/c['hwrm_portrait_candidate']) as f:assert f.size==(384,192)
    assert len(dialogue)==500
    audio_count=0;seconds=0
    for cue in dialogue:
        assert cue['key'] in text and cue['character_ids']
        for name in cue['character_ids']:assert any(c['id']==name for c in portraits)
        a=cue['english_audio']
        if not a:continue
        for field in ('wav','wem'):assert hashlib.sha256((OUT/a[field]).read_bytes()).hexdigest()==a[field+'_sha256']
        with wave.open(str(OUT/a['wav']),'rb') as f:assert abs(f.getnframes()/f.getframerate()-a['seconds'])<0.000002
        audio_count+=1;seconds+=a['seconds']
    timelines=read(OUT/'manifests/timelines.json')
    assert sum(len(t['clips']) for t in timelines)==125
    for t in timelines:
        for clip in t['clips']:assert clip['key'] in text
    report={'game_launched':False,'reviewed_original_strings':len(text)-3,'lua_files_parsed':lua_count,'mission_order':expected,'maps':maps,'explicit_native_requests':sum(m['explicit_native_requests'] for m in maps),'group_count':sum(len(m['groups']) for m in manifest['missions']),'loading_images':len(loading),'source_portrait_variants':read(OUT/'manifests/media-verification.json')['portrait_variants'],'dialogue_keys':len(dialogue),'audio_decoded_and_hash_checked':audio_count,'total_audio_seconds':round(seconds,2),'missing_audio':[s['key'] for s in dialogue if not s['english_audio']],'timeline_clips':125,'scope':'Syntax, source coverage, data wiring, image decoding and audio integrity. Native engine behavior, battle balance, native speech playback and speech actors remain untested.'}
    checks=OUT/'checks';checks.mkdir(exist_ok=True)
    (checks/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('maps','mission_order')},ensure_ascii=False))


if __name__=='__main__':main()
