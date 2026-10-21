"""Prepare native campaign subtitles/portraits and separate animatic speech.

Uses the shipped ui/subtitle.lua, SCAR_Util.lua and A00_speech.lua conventions.
Does not launch or install HWRM. Original audio/video sources remain untouched.
"""
import concurrent.futures
import hashlib
import json
import re
import shutil
import subprocess
import wave
from pathlib import Path

from PIL import Image,ImageOps
from lupa.lua51 import LuaRuntime
from apply_campaign_movies import ROOT,add_wrappers,movie_name

WORK=ROOT/'local/campaign-speech'
SOURCE=WORK/'source'
RESOURCES=WORK/'resources'
MOVIES=WORK/'release-movies'
FFMPEG=ROOT/'local/cinematic-preparation/ffmpeg.exe'
ACTORS={
    'Character_Tyrra':(27,'tyrra'),
    'Character_Karan_OutofTank':(28,'karan'),
    'Character_Karan':(28,'karan'),
    'Character_FleetIntelligence':(29,'intelligence'),
    'Character_Giitan_Radaa':(30,'giitan'),
    'Character_Amma_Radaa':(31,'amma'),
}


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def pcm(source,target):
    target.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run([str(FFMPEG),'-y','-hide_banner','-loglevel','error','-i',str(source),'-map_metadata','-1','-ac','1','-ar','44100','-c:a','pcm_s16le',str(target)],check=True)
    # Keep a plain PCM RIFF header, avoiding modern encoder metadata chunks.
    with wave.open(str(target)) as w:frames=w.readframes(w.getnframes())
    with wave.open(str(target),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(44100);w.writeframes(frames)
    target.with_suffix('.lua').write_text('version=4\ncompression=0\nvolume=0.85\nrandSampContainer=0\n',encoding='ascii')
    with wave.open(str(target)) as w:
        assert (w.getnchannels(),w.getframerate(),w.getsampwidth())==(1,44100,2)
        return w.getnframes()/44100


RUNTIME='''-- Native Subtitle_Add uses ui/subtitle.lua themes and numbered PCM WAVs.
VRC_Speech = __LINES__
function VRC_LineReady()
    if VRC_ActiveActor ~= nil then return Subtitle_IsDone(VRC_ActiveActor) end
    if VRC_Time >= VRC_NextLine then return 1 end
    return 0
end
function VRC_QueueDone()
    if VRC_QueueIndex > getn(VRC_Queue) and VRC_LineReady() ~= 0 then return 1 end
    return 0
end
function VRC_PlayLine(key,duration)
    local speech=VRC_Speech[key]
    VRC_ActiveActor=nil
    if speech ~= nil then
        VRC_ActiveActor=speech.actor
        Subtitle_Add(speech.actor,VRC_Text[key],speech.duration)
        return speech.duration
    end
    Subtitle_Message(VRC_Text[key],duration)
    return duration
end
function VRC_KeepDialogueAndFinish(key)
    local pending={}
    for i=VRC_QueueIndex,getn(VRC_Queue) do
        local queued=VRC_Queue[i]
        if VRC_Speech[queued] ~= nil then pending[getn(pending)+1]=queued end
    end
    VRC_Queue=pending
    VRC_QueueIndex=1
    VRC_Line(key)
end
'''


def bind(target):
    base=target/'leveldata/campaign/VastReachesMiniCampaign'
    for path in base.glob('*/*.lua'):
        if path.stem==path.parent.name:
            text=path.read_text(encoding='ascii').replace('VRC_Lines({"prototype",','VRC_Lines({')
            path.write_text(text,encoding='ascii')
    common=base/'VRC_Common.lua';text=common.read_text(encoding='ascii')
    text=text.replace('    VRC_Queue = {}\n    VRC_QueueIndex = 1\n    VRC_NextLine = VRC_Time\n    VRC_Line(key)',
                      '    VRC_KeepDialogueAndFinish(key)')
    if 'VRC_Speech.lua' in text:
        common.write_text(text,encoding='ascii')
        return
    text+='\ndofilepath("data:leveldata/campaign/VastReachesMiniCampaign/VRC_Speech.lua")\n'
    text=text.replace('    VRC_QueueIndex = 1\n    VRC_NextLine = 0','    VRC_QueueIndex = 1\n    VRC_ActiveActor = nil\n    Sound_SpeechSubtitlePath("data:sound/speech/missions/VRC/")\n    VRC_NextLine = 0',1)
    text=text.replace('if VRC_Time >= VRC_EndTime then','if VRC_Time >= VRC_EndTime and VRC_QueueDone() ~= 0 then')
    text=text.replace('VRC_Time >= VRC_NextLine and VRC_QueueIndex <= getn(VRC_Queue)','VRC_LineReady() ~= 0 and VRC_QueueIndex <= getn(VRC_Queue)')
    text=text.replace('        Subtitle_Message(VRC_Text[key],duration)','        duration=VRC_PlayLine(key,duration)')
    # Grant is forced/free, but the option must be unblocked while granting.
    text=text.replace('for j=1,getn(requirements) do Player_GrantResearchOption(0,requirements[j]) end',
        'for j=1,getn(requirements) do\n                Player_UnrestrictResearchOption(0,requirements[j])\n                Player_GrantResearchOption(0,requirements[j])\n                Player_RestrictResearchOption(0,requirements[j])\n            end')
    common.write_text(text,encoding='ascii')
    t1=base/'T01_Training/T01_Training.lua'
    text=t1.read_text(encoding='ascii')
    text=text.replace('VRC_QueueIndex <= getn(VRC_Queue) or VRC_Time < VRC_NextLine','VRC_QueueDone() == 0')
    t1.write_text(text,encoding='ascii')


def movie_bed(entry):
    package=ROOT/'campaign-export/cinematics'/entry['directory']
    manifest=json.loads((package/'manifest.json').read_text(encoding='utf8'))
    render=json.loads((ROOT/'local/cinematic-update/render'/entry['directory']/'render.json').read_text(encoding='utf8'))
    stems=[]
    for row in manifest['stems']:
        stems.extend([{**item,'event':row['event']} for item in row['media']] if 'media' in row else [row])
    result=[]
    for language,short in (('English','en'),('Russian','ru')):
        target=MOVIES/language/(movie_name(entry['directory'])+'.webm');target.parent.mkdir(parents=True,exist_ok=True)
        cmd=[str(FFMPEG),'-y','-hide_banner','-loglevel','error','-i',str(ROOT/f'local/cinematic-update/movies/{entry["directory"]}.{short}.webm')]
        filters=[];labels=[]
        for i,stem in enumerate(stems,1):
            cmd+=['-i',str(package/stem['wav'])]
            gain=.28 if 'music' in stem.get('event',str(stem.get('short_name',''))).lower() else .35
            layout='pan=stereo|c0=0.75*c0+0.25*c2|c1=0.75*c1+0.25*c3' if stem['channels']==4 else 'aformat=channel_layouts=stereo'
            filters.append(f'[{i}:a]{layout},volume={gain}[s{i}]');labels.append(f'[s{i}]')
        if labels:filters.append(''.join(labels)+f'amix=inputs={len(labels)}:duration=longest:normalize=0,alimiter=limit=0.95:level=false,apad[a]')
        else:filters.append('anullsrc=r=44100:cl=stereo[a]')
        cmd+=['-filter_complex',';'.join(filters),'-map','0:v','-map','[a]','-c:v','copy','-c:a','libvorbis','-q:a','5','-ar','44100','-map_metadata','-1','-disposition:v','default','-disposition:a','default','-cluster_time_limit','1000','-cluster_size_limit','1048576','-t',str(render['duration_seconds']),str(target)]
        subprocess.run(cmd,check=True)
        result.append({'path':target.relative_to(MOVIES).as_posix(),'sha256':sha(target),'bytes':target.stat().st_size,'narration_embedded':False})
    return result


def prepare(seed=None,convert_movies=True):
    seed=Path(seed or ROOT/'local/cinematic-update/source')
    WORK.mkdir(parents=True,exist_ok=True)
    if not (WORK/'baseline-release').exists():shutil.copytree(ROOT/'local/VastReachesCampaignDemo-release',WORK/'baseline-release')
    if SOURCE.exists():assert (SOURCE/'campaign-speech-id.txt').read_text().strip()=='VRC-native-speech-v1'
    shutil.copytree(seed,SOURCE,dirs_exist_ok=True)
    (SOURCE/'campaign-speech-id.txt').write_text('VRC-native-speech-v1\n',encoding='ascii')
    RESOURCES.mkdir(parents=True,exist_ok=True)
    base=SOURCE/'leveldata/campaign/VastReachesMiniCampaign'
    vm=LuaRuntime();vm.execute((base/'VRC_Data.lua').read_text(encoding='ascii'))
    texts=dict(vm.globals().VRC_Text.items())
    used={key for p in base.glob('*/*.lua') for key in re.findall(r'"([MT]\d\d_[^"\n]+)"',p.read_text(encoding='ascii')) if key in texts}
    rows={r['key']:r for r in json.loads((ROOT/'campaign-export/manifests/dialogue.json').read_text(encoding='utf8'))}
    lines={};report=[]
    for key in sorted(used):
        if key not in rows:
            assert not re.match(r'[MT]\d\d_\d\d\d_',key),'Missing dialogue definition: '+key
            continue  # Objectives/status messages retain the generic region.
        row=rows[key];assert len(row['character_ids'])==1,(key,row['character_ids'])
        char=row['character_ids'][0];actor,_=ACTORS[char];audio=row['english_audio'];assert audio,key
        target=RESOURCES/f'sound/speech/missions/VRC/{texts[key][1:]}.wav'
        duration=pcm(ROOT/'campaign-export'/audio['wav'],target)
        lines[key]={'actor':actor,'duration':round(duration+.25,6)}
        report.append({'key':key,'text':texts[key],'character':char,'actor':actor,'duration':duration,'path':target.relative_to(RESOURCES).as_posix()})
    lua='{'+','.join('['+json.dumps(k)+']={actor='+str(v['actor'])+',duration='+str(v['duration'])+'}' for k,v in sorted(lines.items()))+'}'
    runtime=RUNTIME.replace('__LINES__',lua)
    (base/'VRC_Speech.lua').write_text(runtime,encoding='ascii')
    themes=(ROOT/'local/hwrm-base/ui/subtitle.lua').read_text(encoding='ascii')
    portraits={name:(slot,short) for name,(slot,short) in ACTORS.items() if name!='Character_Karan'}
    for name,(slot,short) in portraits.items():
        themes=re.sub(r'addTheme\('+str(slot)+r',[^\n]+',f'addTheme({slot}, {{255,255,255}}, 0.1, 0.1, 0,"VRC_{short}#.tga",1)',themes)
        image=Image.open(ROOT/f'campaign-export/assets/portraits/{name}.png').convert('RGBA')
        image=ImageOps.contain(image,(384,192),Image.Resampling.LANCZOS)
        canvas=Image.new('RGBA',(384,192));canvas.alpha_composite(image,((384-image.width)//2,(192-image.height)//2))
        target=RESOURCES/f'ui/speechicons/VRC_{short}0.tga';target.parent.mkdir(parents=True,exist_ok=True);canvas.save(target)
    (RESOURCES/'ui/subtitle.lua').write_text(themes,encoding='ascii')
    index=json.loads((ROOT/'campaign-export/cinematics/index.json').read_text(encoding='utf8'))['scenes']
    cues=[];movie_audio=[]
    for entry in index:
        package=ROOT/'campaign-export/cinematics'/entry['directory'];manifest=json.loads((package/'manifest.json').read_text(encoding='utf8'))
        name=movie_name(entry['directory']);script=[f'SetSpeechFolder("data:sound/speech/animatic/VRC/{name}")']
        voice=package/('audio/prologue_voice_timeline.wav' if entry['directory']=='prologue' else manifest['voice_reference']['reference'])
        track=RESOURCES/f'sound/music/animatic/VRC/{name}.wav'
        duration=pcm(voice,track)
        movie_audio.append({'movie':name,'path':track.relative_to(RESOURCES).as_posix(),'duration':duration,'sha256':sha(track)})
        for cue in manifest['dialogue_cues']:
            if cue.get('effectively_muted'):continue
            script.append(f'AddSpeechEvent({cue["start"]:.9f},"{cue["key"]}")')
            cues.append({'movie':name,'key':cue['key'],'start':cue['start']})
        for target in (SOURCE,ROOT/'minicampaign',ROOT/'campaign-export/data'):
            for language in ('English','Russian'):
                path=target/f'locale/{language}/{name}_speech.lua';path.parent.mkdir(parents=True,exist_ok=True);path.write_text('\n'.join(script)+'\n',encoding='ascii')
    for target in (SOURCE,ROOT/'minicampaign'):
        shutil.copytree(RESOURCES,target,dirs_exist_ok=True)
        (target/'leveldata/campaign/VastReachesMiniCampaign/VRC_Speech.lua').write_text(runtime,encoding='ascii')
        bind(target)
    # The standalone full preparation needs animatic audio too; gameplay speech
    # for its unimplemented chapters remains a separate stage.
    shutil.copytree(RESOURCES/'sound',ROOT/'campaign-export/data/sound',dirs_exist_ok=True)
    for target in (SOURCE,ROOT/'minicampaign',ROOT/'campaign-export/data'):add_wrappers(target,index)
    MOVIES.mkdir(exist_ok=True);(MOVIES/'vre-movies-id.txt').write_text('VRC-rendered-campaign-movies-v1\n',encoding='ascii')
    if convert_movies:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:videos=[v for result in pool.map(movie_bed,index) for v in result]
    else:videos=json.loads((WORK/'integration.json').read_text(encoding='utf8'))['movies']
    integration={'enabled':True,'source':str(SOURCE),'mission_lines':report,'animatic_cues':cues,'animatic_audio_mode':'movie_owned','movie_audio':movie_audio,'movies':videos,'native_tested':False,'previous_movie_loop_cause':'not established; narration moved outside WebM; separate speech events survived skip, now use Movie.filenameA','stock_actors_untouched':True,'game_launched':False}
    save(WORK/'integration.json',integration)
    print(json.dumps({'source':str(SOURCE),'mission_lines':len(report),'animatic_cues':len(cues),'music_only_videos':len(videos),'native_tested':False}))
    return SOURCE


if __name__=='__main__':prepare()
