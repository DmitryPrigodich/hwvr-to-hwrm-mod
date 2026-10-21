"""Extract the original VR prologue components without running either game.

This is a source package, not a faithful flattened video render or a Wwise mix.
"""
from __future__ import annotations

import hashlib
from array import array
import json
import shutil
import subprocess
import wave
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import UnityPy
from PIL import Image, ImageDraw, ImageFont, ImageOps
from UnityPy.export.Texture2DConverter import parse_image_data

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'local/quest-content/HomeworldVastReachesDemo_Data'
OUT = ROOT / 'campaign-export/cinematics/prologue'
ASSET = 'sharedassets25.assets'
SCENE = 'level25'


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def srt_time(seconds):
    milliseconds = round(seconds * 1000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    raw = {name: json.loads((ROOT/f'local/quest-audit/{name}.json').read_text(encoding='utf8')) for name in (ASSET, SCENE)}
    by_id = {r['path_id']: r for r in raw[ASSET]}
    timeline = next(t for t in json.loads((ROOT/'campaign-export/manifests/timelines.json').read_text(encoding='utf8')) if t['mission'] == 'Mission_T1')
    end = max(r['data']['m_Time'] for r in raw[ASSET] if r['class_name'] == 'UnityEngine.Timeline.SignalEmitter')
    assert end == 143.25
    tracks = []
    for row in raw[ASSET]:
        if 'm_Clips' not in row['data']:
            continue
        parent = row['data'].get('m_Parent', {}).get('m_PathID')
        muted = bool(row['data'].get('m_Muted'))
        visited = set()
        while parent in by_id and parent not in visited:
            visited.add(parent)
            muted |= bool(by_id[parent]['data'].get('m_Muted'))
            parent = by_id[parent]['data'].get('m_Parent', {}).get('m_PathID')
        tracks.append({'path_id': row['path_id'], 'class_name': row['class_name'], 'name': row['data'].get('m_Name'), 'effectively_muted': muted, 'data': row['data']})
    save_json(OUT/'source/timeline.json', {'scene': timeline['scene'], 'end_signal_seconds': end, 'tracks': tracks, 'records': raw[ASSET]})
    save_json(OUT/'source/scene-audit.json', raw[SCENE])

    env = UnityPy.Environment()
    env.path = str(GAME.resolve())
    env.load_file(str((GAME/ASSET).resolve()))
    image_rows = []
    faces = ('positive_x', 'negative_x', 'positive_y', 'negative_y', 'positive_z', 'negative_z')
    for obj in env.objects:
        if obj.assets_file.name != ASSET or obj.type.name not in ('Cubemap', 'Sprite'):
            continue
        asset = obj.parse_as_object()
        if obj.type.name == 'Cubemap':
            data = asset.get_image_data()
            assert asset.m_ImageCount == 6 and asset.m_MipCount == 1
            assert len(data) == asset.m_CompleteImageSize * 6
            for i, face in enumerate(faces):
                image = parse_image_data(data[i*asset.m_CompleteImageSize:(i+1)*asset.m_CompleteImageSize], asset.m_Width, asset.m_Height, asset.m_TextureFormat, obj.version, obj.platform, getattr(asset, 'm_PlatformBlob', None), flip=False)
                dest = OUT/f'images/{asset.m_Name}/{face}.png'
                dest.parent.mkdir(parents=True, exist_ok=True)
                image.save(dest)
                image_rows.append({'name': asset.m_Name, 'face': face, 'source': ASSET, 'path_id': obj.path_id, 'path': dest.relative_to(OUT).as_posix(), 'size': list(image.size)})
        else:
            image = asset.image.convert('RGBA')
            dest = OUT/f'images/{asset.m_Name}.png'
            dest.parent.mkdir(parents=True, exist_ok=True)
            image.save(dest)
            image_rows.append({'name': asset.m_Name, 'source': ASSET, 'path_id': obj.path_id, 'path': dest.relative_to(OUT).as_posix(), 'size': list(image.size)})

    sheet = Image.new('RGB', (1200, 4*235+230), '#111923')
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 14)
    cubes = list(dict.fromkeys(r['name'] for r in image_rows if 'face' in r))
    for y, name in enumerate(cubes):
        draw.text((8, y*235+5), name, font=font, fill='white')
        for x, row in enumerate(r for r in image_rows if r['name'] == name):
            image = ImageOps.contain(Image.open(OUT/row['path']).convert('RGB'), (194, 194))
            sheet.paste(image, (x*200+3, y*235+27))
            draw.text((x*200+4, y*235+221), row['face'], font=font, fill='white')
    for i, row in enumerate(r for r in image_rows if 'face' not in r):
        image = ImageOps.contain(Image.open(OUT/row['path']).convert('RGB'), (190,190))
        sheet.paste(image, (i*400+5, 4*235+5))
        draw.text((i*400+5,4*235+199),row['name'],font=font,fill='white')
    sheet.save(OUT/'source-contact.jpg', quality=90)

    dialogues = {r['key']: r for r in json.loads((ROOT/'campaign-export/manifests/dialogue.json').read_text(encoding='utf8'))}
    locale = json.loads((ROOT/'campaign-export/manifests/localization.json').read_text(encoding='utf8'))
    sample_rate = 48000
    voice = bytearray(round(end*sample_rate)*4)
    cues = []
    previous_end = 0
    for clip in timeline['clips']:
        cue = dialogues[clip['key']]
        assert cue['english_audio']
        src = ROOT/'campaign-export'/cue['english_audio']['wav']
        target = OUT/f'audio/{src.name}'
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
        with wave.open(str(src), 'rb') as stream:
            assert stream.getsampwidth() == 2 and stream.getframerate() == sample_rate
            channels = stream.getnchannels()
            pcm = array('h')
            pcm.frombytes(stream.readframes(stream.getnframes()))
        if channels == 1:
            stereo = array('h', [0])*(len(pcm)*2)
            stereo[0::2] = pcm
            stereo[1::2] = pcm
            pcm = stereo
        else:
            assert channels == 2
        start = round(clip['start']*sample_rate)
        count = min(len(pcm)//2,round(clip['duration']*sample_rate),len(voice)//4-start)
        assert start >= previous_end, 'Overlapping voice clips need a real mixer'
        voice[start*4:(start+count)*4] = pcm[:count*2].tobytes()
        previous_end = start+count
        cues.append({**clip, 'audio': target.relative_to(OUT).as_posix(), 'en': locale[clip['key']]['en'], 'ru': locale[clip['key']]['ru'], 'origin': cue['english_audio']['source']})
    with wave.open(str(OUT/'audio/prologue_voice_timeline.wav'),'wb') as stream:
        stream.setparams((2,2,sample_rate,0,'NONE','not compressed'))
        stream.writeframes(voice)
    for language in ('en','ru'):
        (OUT/f'prologue.{language}.srt').write_text('\n\n'.join(f"{i}\n{srt_time(c['start'])} --> {srt_time(c['start']+c['duration'])}\n{c[language]}" for i,c in enumerate(cues,1))+'\n', encoding='utf8')

    sound_root = ET.parse(GAME/'StreamingAssets/Audio/GeneratedSoundBanks/Windows/SoundbanksInfo.xml').getroot()
    wanted = ('play_music_animatic_m_01','play_sfx_amb_bed_animatic_mission_01')
    events = {e.attrib['Name']: e for e in sound_root.iter('Event') if e.attrib['Name'] in wanted}
    media = {f.attrib['Id']: f for f in sound_root.iter('File') if f.attrib.get('Language') == 'SFX'}
    quest = Path(r'G:\Games\HW_Games\Homeworld- Vast Reaches v16520+1.1.0-16520 -VRP')
    stems = []
    with zipfile.ZipFile(next(quest.rglob('*.obb'))) as archive:
        for name in wanted:
            event = events[name]
            ids = [m.attrib['Id'] for m in event.iter('MediaRef')]
            assert len(ids) == 1
            file = media[ids[0]]
            member = 'assets/Audio/GeneratedSoundBanks/Windows/'+file.findtext('Path').replace('\\','/')
            wem = OUT/f'audio/{name}.wem'
            wem.write_bytes(archive.read(member))
            wav = wem.with_suffix('.wav')
            if not wav.exists():
                subprocess.run([str(ROOT/'local/vgmstream/vgmstream-cli.exe'),'-i','-o',str(wav),str(wem)], capture_output=True, check=True)
            with wave.open(str(wav),'rb') as stream:
                info = {'seconds':stream.getnframes()/stream.getframerate(),'channels':stream.getnchannels(),'sample_rate':stream.getframerate(),'sample_width':stream.getsampwidth()}
            stems.append({'event':name,'event_id':event.attrib['Id'],'media_id':ids[0],'short_name':file.findtext('ShortName'),'quest_member':member,'wem':wem.relative_to(OUT).as_posix(),'wav':wav.relative_to(OUT).as_posix(),**info})

    report = {'status':'source_components_extracted; no_flattened_video; not_installed; not_engine_tested', 'version':'Quest 1.1.0-16520', 'duration_seconds':end, 'dialogue_cues':cues, 'images':image_rows, 'stems':stems, 'notes':['Voice-only reference follows original Timeline starts and trims at clip duration.', 'Music and ambience remain original separate stems: Wwise bus gains and transition timing are not reconstructed.', 'Cube faces preserve Unity face order and are decoded without a vertical flip; final projection/view must be reviewed.', '3D animated ships, nested PlayableDirectors, camera composition and fades still need rendering/adaptation. A skybox slideshow would not reproduce the original.']}
    save_json(OUT/'manifest.json',report)
    files = sorted(p for p in OUT.rglob('*') if p.is_file() and p.name != 'SHA256SUMS.txt')
    (OUT/'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(OUT).as_posix()}\n' for p in files),encoding='utf8')
    print(json.dumps({'directory':str(OUT),'duration_seconds':end,'images':len(image_rows),'voice_cues':len(cues),'stems':stems,'status':report['status']},ensure_ascii=False))


if __name__ == '__main__':
    main()
