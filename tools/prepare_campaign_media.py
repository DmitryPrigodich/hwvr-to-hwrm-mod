"""Extract original campaign UI/audio; stage honest, reviewable HWRM import assets.

Does not launch Unity/HWRM, synthesize voices, or disguise WAV as Relic FDA.
WEM decoding uses the upstream vgmstream CLI in local/vgmstream.
"""
import collections
import concurrent.futures
import csv
import hashlib
import json
import re
import shutil
import subprocess
import wave
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps
from compare_quest_steam import load

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'campaign-export'
RAW=ROOT/'local/quest-audit'
DATA=ROOT/'local/quest-campaign'
GAME=ROOT/'local/quest-content/HomeworldVastReachesDemo_Data'
QUEST=Path(r'G:\Games\HW_Games\Homeworld- Vast Reaches v16520+1.1.0-16520 -VRP')
STEAM=Path(r'C:\Program Files (x86)\Steam\steamapps\common\Homeworld Vast Reaches Demo\HomeworldVastReachesDemo_Data')
DECODER=ROOT/'local/vgmstream/vgmstream-cli.exe'
CHAPTERS=['T01_Training','M01_ProvingGrounds','M07_AngelMoon','M03_GybbasRaid','M04_LostDestroyer','M05_HiigaraShipyard','M06_Weapon','M09_Tenhauser','M10_OuterReef','M11_WeaponArchitects','M08_GybbasOffensive','M13_ReturnToHiigara']


def save_json(path, data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


def main():
    metadata=json.loads((RAW/'index.json').read_text())
    text=json.loads((OUT/'manifests/localization.json').read_text(encoding='utf8'))
    cache={}
    def rows(source):
        if source not in cache:
            p=RAW/(source+'.json')
            cache[source]={r['path_id']:r for r in json.loads(p.read_text(encoding='utf8'))} if p.exists() else {}
        return cache[source]
    def address(owner,ref):
        if not ref or not ref.get('m_PathID'):return None
        source=owner['source']
        if ref.get('m_FileID'):source=metadata['files'][source]['externals'][ref['m_FileID']-1]
        return source,ref['m_PathID']
    def ptr(owner,ref):
        a=address(owner,ref)
        return rows(a[0]).get(a[1]) if a else None
    def records(cls):
        sources={r['source'] for r in metadata['mono_types'] if r['class_name']==cls}
        return [r for source in sorted(sources) for r in rows(source).values() if r['class_name']==cls]
    print('Loading source images',flush=True)
    env=load(GAME); objects={(o.assets_file.name,o.path_id):o for o in env.objects}
    image_cache={}; failures=[]
    def sprite(owner,ref,target):
        a=address(owner,ref)
        if not a:return None
        if a in image_cache:return image_cache[a]
        try:
            o=objects[a]; asset=o.parse_as_object(); img=asset.image.convert('RGBA')
            path=OUT/'assets'/target; path.parent.mkdir(parents=True,exist_ok=True); img.save(path)
            info={'path':path.relative_to(OUT).as_posix(),'source':a[0],'path_id':a[1],'name':asset.m_Name,'width':img.width,'height':img.height,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
            image_cache[a]=info; return info
        except Exception as exc:
            failures.append({'source':a,'target':str(target),'error':str(exc)});return None
    names={
        'Character_Name_Amma':('Amma Radaa','Амма Радаа'),
        'Character_Name_Giitan':('Giitan Radaa','Гиитан Радаа'),
        'Character_Name_FleetIntelligence':('Fleet Intelligence','Разведка флота'),
        'Character_Name_Karan':('Karan S’jet','Каран С’Джет'),
        'Character_Name_Karan_OutofTank':('Karan S’jet','Каран С’Джет'),
        'Character_Name_Tyrra':('Tyrra Soban','Тирра Собан'),
        'Character_Name_ScienceOfficerHauk':('Hauk','Хаук'),
        'Character_Name_SOHauk':('Chief Engineer Hauk','Главный инженер Хаук'),
        'Character_Name_Bentusi':('Bentusi','Бентуси'),
        'Character_Name_Narrator':('Narrator','Рассказчик'),
    }
    original_en={k:v for t in json.loads((DATA/'strings-en.json').read_text(encoding='utf8')).values() for k,v in t.items()}
    character_map={}; characters=[]
    for char in records('Hercules.Character'):
        stem=re.sub(r'[^\w-]+','_',char['name'])
        portrait=sprite(char,char['data']['_characterPortrait'],Path('portraits')/(stem+'.png'))
        grey=sprite(char,char['data']['_grayscalePortrait'],Path('portraits')/(stem+'-grey.png'))
        key=char['data']['_characterNameKey']; pair=names.get(key,(original_en.get(key,key),original_en.get(key,key)))
        info={'id':stem,'source':char['source'],'path_id':char['path_id'],'name_key':key,'en':pair[0],'ru':pair[1],'portrait':portrait,'grayscale':grey}
        characters.append(info); character_map[(char['source'],char['path_id'])]=info
        # Native-sized transparent canvas, prepared for speech UI review; no stock actor overridden.
        if portrait:
            image=Image.open(OUT/portrait['path']).convert('RGBA')
            icon=Image.new('RGBA',(384,192)); head=ImageOps.contain(image,(192,192),Image.Resampling.LANCZOS)
            icon.alpha_composite(head,((384-head.width)//2,(192-head.height)//2))
            target=OUT/f'data/ui/vastreaches/portraits/{stem}.tga';target.parent.mkdir(parents=True,exist_ok=True);icon.save(target)
            info['hwrm_portrait_candidate']=target.relative_to(OUT).as_posix()
            info['portrait_binding_status']='prepared_for_custom_speech_actor_review'
    missions=json.loads((DATA/'missions.json').read_text(encoding='utf8'))
    missions=[m for m in missions if m['category']=='_tutorialMissions']+[m for m in missions if m['category']=='_campaignMissions']
    previews=[]
    for m,chapter in zip(missions,CHAPTERS):
        definition=rows(m['source'])[m['path_id']]
        image=sprite(definition,definition['data']['_missionPreviewSprite'],Path('loading')/(m['id']+'.png'))
        info={'mission':m['id'],'chapter':chapter,'image':image,'provenance':'Original MissionDefinition._missionPreviewSprite; not a pre-rendered cinematic.'}
        if image:
            target=OUT/f'data/leveldata/campaign/VastReachesFull/{chapter}/{chapter}.dds';target.parent.mkdir(parents=True,exist_ok=True)
            Image.open(OUT/image['path']).convert('RGB').save(target,pixel_format='DXT1')
            info['hwrm_loading_dds']=target.relative_to(OUT).as_posix()
        previews.append(info)
    del objects,env
    audio=collections.defaultdict(list)
    soundbank=ET.parse(GAME/'StreamingAssets/Audio/GeneratedSoundBanks/Windows/SoundbanksInfo.xml').getroot()
    media={f.attrib['Id']:{'id':f.attrib['Id'],'name':f.findtext('ShortName'),'path':f.findtext('Path')} for f in soundbank.iter('File') if f.attrib.get('Language')=='English(US)'}
    events={e.attrib['Id']:{'name':e.attrib['Name'],'media':[m.attrib['Id'] for m in e.iter('MediaRef')]} for e in soundbank.iter('Event')}
    for row in media.values():audio[Path(row['name']).stem].append(row)
    lines=collections.defaultdict(list)
    for row in records('Hercules.DialogueLine'):
        if row['data']['_textKey'] in text:lines[row['data']['_textKey']].append(row)
    obb=next(QUEST.rglob('*.obb'))
    sounds=[]; tasks=[]
    with zipfile.ZipFile(obb) as archive:
        paths=set(archive.namelist())
        for key,variants in sorted(lines.items()):
            variant_info=[]
            for row in variants:
                char=character_map.get(address(row,row['data']['_character']))
                event=ptr(row,row['data'].get('_wwiseDialogueEvent',{}).get('WwiseObjectReference'))
                variant_info.append({'source':row['source'],'path_id':row['path_id'],'duration':row['data']['_duration'],'character_id':char['id'] if char else None,'wwise_event':event['data'].get('objectName') if event else None,'wwise_event_id':event['data'].get('id') if event else None})
            char_ids=sorted({v['character_id'] for v in variant_info if v['character_id']})
            bound_ids={mid for v in variant_info for mid in events.get(str(v['wwise_event_id']),{}).get('media',[]) if mid in media}
            candidates=[media[mid] for mid in sorted(bound_ids)] if bound_ids else audio[key]
            info={'key':key,'ucs_id':text[key]['id'],'en':text[key]['en'],'ru':text[key]['ru'],'character_ids':char_ids,'definitions':variant_info,'english_audio':None,'audio_status':'unresolved'}
            if len(candidates)==1:
                entry=candidates[0]; media_id=entry['id']; name='assets/Audio/GeneratedSoundBanks/Windows/'+entry['path'].replace('\\','/')
                destination=OUT/f'assets/audio/wem/{key}.wem';destination.parent.mkdir(parents=True,exist_ok=True)
                if name in paths:
                    destination.write_bytes(archive.read(name));origin={'container':obb.name,'member':name,'version':'Quest 1.1.0-16520'}
                else:
                    fallback=STEAM/'StreamingAssets/Audio/GeneratedSoundBanks/Windows'/entry['path']
                    if fallback.exists():
                        shutil.copy2(fallback,destination);origin={'path':str(fallback),'version':'Steam 1.2.0-25236','note':'Exact English text matches the Quest script.'}
                    else:origin=None
                if origin:
                    wav=OUT/f'assets/audio/wav/{key}.wav';wav.parent.mkdir(parents=True,exist_ok=True)
                    info['english_audio']={'media_id':media_id,'short_name':entry['name'],'binding':'DialogueLine -> WwiseEventReference.id -> SoundbanksInfo.Event.MediaRef' if bound_ids else 'unique matching ShortName','source':origin,'wem':destination.relative_to(OUT).as_posix(),'wav':wav.relative_to(OUT).as_posix(),'wem_sha256':hashlib.sha256(destination.read_bytes()).hexdigest()}
                    info['audio_status']='native_speech_binding_pending';tasks.append((destination,wav,info))
                else:info['audio_status']='media_not_loose_in_quest_or_steam; inspect_embedded_bank'
            else:info['audio_status']=f'logical_media_candidates_{len(candidates)}'
            sounds.append(info)
    print(f'Decoding {len(tasks)} original English cues',flush=True)
    def decode(task):
        wem,wav,info=task
        if not wav.is_file():
            run=subprocess.run([str(DECODER),'-i','-o',str(wav),str(wem)],capture_output=True,text=True)
            if run.returncode:raise RuntimeError(info['key']+': '+run.stderr[-500:])
        with wave.open(str(wav),'rb') as f:
            a=info['english_audio'];a.update({'seconds':round(f.getnframes()/f.getframerate(),6),'channels':f.getnchannels(),'sample_rate':f.getframerate(),'sample_width':f.getsampwidth(),'frames':f.getnframes()})
            assert f.getnframes()>0
        a['wav_sha256']=hashlib.sha256(wav.read_bytes()).hexdigest()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(decode,tasks))
    save_json(OUT/'manifests/characters.json',characters)
    save_json(OUT/'manifests/loading.json',previews)
    save_json(OUT/'manifests/dialogue.json',sounds)
    # A sharedassets file can contain multiple scenes' timelines (notably M7/M9).
    from campaign_cinematic_sources import scan_scenes, timeline_manifest
    _, cinematic_scenes = scan_scenes()
    timelines = timeline_manifest(cinematic_scenes)
    save_json(OUT/'manifests/timelines.json',timelines)
    lua=['-- Original English audio prepared as WAV/WEM. Native speech and actor bindings are pending; stock tutorial uses PCM WAV.','VRE_AudioDuration = {}','VRE_Dialogue = {}']
    for info in sounds:
        audio=info['english_audio'];key=info['key']
        duration=audio['seconds'] if audio else max(v['duration'] for v in info['definitions'])
        lua.append(f'VRE_AudioDuration["{key}"] = {duration:.6f}')
        char=info['character_ids'][0] if len(info['character_ids'])==1 else ''
        lua.append(f'VRE_Dialogue["{key}"] = {{text="${info["ucs_id"]}",character="{char}",audioReady=0}}')
    (OUT/'data/scripts/VRE_Dialogue.lua').write_text('\n'.join(lua)+'\n',encoding='ascii')
    with (OUT/'manifests/dialogue.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['key','EN','RU','characters','WAV','seconds','status'])
        for d in sounds:
            a=d['english_audio'] or {};w.writerow([d['key'],d['en'],d['ru'],';'.join(d['character_ids']),a.get('wav',''),a.get('seconds',''),d['audio_status']])
    # Contact sheets are inspection aids; runtime uses the extracted source images.
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for label,items in [('portraits',[(c['id'],c['portrait']) for c in characters if c['portrait']]),('loading',[(p['mission'],p['image']) for p in previews if p['image']])]:
        sheet=Image.new('RGB',(900,((len(items)+3)//4)*200),(18,23,32));draw=ImageDraw.Draw(sheet)
        for i,(title,img) in enumerate(items):
            x=(i%4)*225;y=(i//4)*200
            thumb=ImageOps.contain(Image.open(OUT/img['path']).convert('RGBA'),(215,165))
            sheet.paste(thumb,(x+(225-thumb.width)//2,y),thumb);draw.text((x+5,y+170),title.replace('Character_','')[:26],font=font,fill='white')
        target=OUT/f'previews/{label}.jpg';target.parent.mkdir(parents=True,exist_ok=True);sheet.save(target,quality=92)
    report={'characters':len(characters),'portrait_variants':len([i for i in image_cache.values() if i['path'].startswith('assets/portraits')]),'loading_chapters':len(previews),'dialogue_keys':len(sounds),'decoded_audio':len(tasks),'missing_audio':[s['key'] for s in sounds if s['english_audio'] is None],'character_conflicts':[s['key'] for s in sounds if len(s['character_ids'])!=1],'image_failures':failures,'timeline_scenes':len(timelines),'timeline_clips':sum(len(t['clips']) for t in timelines),'native_audio_status':'Native speech binding pending; stock tutorial PCM WAV route identified; game not launched'}
    save_json(OUT/'manifests/media-verification.json',report)
    print(json.dumps(report,ensure_ascii=False),flush=True)
    assert not failures


if __name__=='__main__':main()
