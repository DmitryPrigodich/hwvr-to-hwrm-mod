"""Prepare the remaining HWVR cinematic source packages, without launching games."""
from __future__ import annotations

import argparse
from array import array
import hashlib
import json
import shutil
import subprocess
import warnings
import wave
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

with warnings.catch_warnings():
    warnings.simplefilter('ignore', DeprecationWarning)
    import audioop

import UnityPy
from PIL import Image, ImageDraw, ImageFont, ImageOps
from UnityPy.export.Texture2DConverter import parse_image_data

from campaign_cinematic_sources import ROOT, scan_scenes, timeline_manifest
from prepare_intro_sources import GAME, save_json, srt_time

OUT = ROOT/'campaign-export/cinematics'
QUEST = Path(r'G:\Games\HW_Games\Homeworld- Vast Reaches v16520+1.1.0-16520 -VRP')
FACES = ('positive_x','negative_x','positive_y','negative_y','positive_z','negative_z')


def identity(source, path_id):
    return {'source':source, 'path_id':path_id}


class Images:
    def __init__(self):
        self.env = UnityPy.Environment()
        self.env.path = str(GAME.resolve())
        self.files = {}

    def get(self, address):
        source, path_id = address
        if source not in self.files:
            self.files[source] = self.env.load_file(str((GAME/source).resolve()))
        return self.files[source].objects[path_id]

    def extract(self, graph, scene, directory):
        wanted = {}
        materials = []
        for clip in scene['visual_clips']:
            data = clip['data']
            usage = {k:clip[k] for k in ('start','duration','effectively_muted','class_name','track')}
            if clip['class_name'] == 'Hercules.BillboardAsset':
                address = graph.address(clip['asset_source'], data.get('Sprite'))
                if address:
                    wanted.setdefault(address, []).append(usage)
            elif clip['class_name'] == 'Hercules.SkyboxControlAsset':
                address = graph.address(clip['asset_source'], data.get('Skybox'))
                if not address:
                    continue
                material = self.get(address).parse_as_dict()
                materials.append({**identity(*address), 'data':material, 'usage':usage})
                for name, texture in material['m_SavedProperties']['m_TexEnvs']:
                    image = graph.address(address[0], texture['m_Texture'])
                    if image:
                        wanted.setdefault(image, []).append({**usage,'material':identity(*address),'texture_property':name})
        result = []
        for address, usage in sorted(wanted.items()):
            obj = self.get(address)
            asset = obj.parse_as_object()
            kind = obj.type.name
            name = asset.m_Name
            basename = f'{address[0].replace(".assets", "")}_{address[1]}_{name}'
            assert not any(c in basename for c in '/\\:*?"<>|'), basename
            common = {**identity(*address), 'name':name, 'kind':kind, 'usage':usage}
            if kind == 'Cubemap':
                data = asset.get_image_data()
                assert asset.m_ImageCount == 6 and asset.m_MipCount >= 1
                assert len(data) == asset.m_CompleteImageSize*6
                assert asset.m_TextureFormat == 50, 'Cubemap mip sizing currently expects source ASTC 6x6'
                base_size = ((asset.m_Width+5)//6)*((asset.m_Height+5)//6)*16
                for index, face in enumerate(FACES):
                    image = parse_image_data(data[index*asset.m_CompleteImageSize:index*asset.m_CompleteImageSize+base_size],asset.m_Width,asset.m_Height,asset.m_TextureFormat,obj.version,obj.platform,getattr(asset,'m_PlatformBlob',None),flip=False)
                    path = directory/f'images/{basename}/{face}.png'
                    path.parent.mkdir(parents=True,exist_ok=True)
                    image.save(path)
                    result.append({**common,'face':face,'source_mip_count':asset.m_MipCount,'exported_mip':0,'path':path.relative_to(directory).as_posix(),'size':list(image.size)})
            else:
                assert kind in ('Sprite','Texture2D'), (address,kind)
                image = asset.image.convert('RGBA')
                path = directory/f'images/{basename}.png'
                path.parent.mkdir(parents=True,exist_ok=True)
                image.save(path)
                result.append({**common,'path':path.relative_to(directory).as_posix(),'size':list(image.size)})
        save_json(directory/'source/skybox-materials.json',materials)
        return result


def contact_sheet(directory, images):
    groups = {}
    for row in images:
        groups.setdefault((row['source'],row['path_id']), []).append(row)
    height = max(1,len(groups))*232
    sheet = Image.new('RGB',(1200,height),'#111923')
    labels = []
    for y, rows in enumerate(groups.values()):
        labels.append(((8,y*232+3),rows[0]['name']))
        for x,row in enumerate(rows):
            with Image.open(directory/row['path']) as original:
                image = ImageOps.contain(original.convert('RGB'),(190,190))
            sheet.paste(image,(x*200+4,y*232+24))
            labels.append(((x*200+4,y*232+215),row.get('face',row['kind'])))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    for position,label in labels:
        draw.text(position,label,font=font,fill='white')
    sheet.save(directory/'source-contact.jpg',quality=90)


def voices(directory, scene, dialogue, locale):
    cues = []
    segments = []
    frames = round(scene['duration_seconds']*48000)
    for clip in scene['clips']:
        cue = dialogue[clip['key']]
        assert cue['english_audio'], clip['key']
        original = ROOT/'campaign-export'/cue['english_audio']['wav']
        target = directory/f'audio/{original.name}'
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(original,target)
        with wave.open(str(target),'rb') as sound:
            assert sound.getsampwidth() == 2 and sound.getframerate() == 48000
            channels = sound.getnchannels()
            pcm = array('h');pcm.frombytes(sound.readframes(sound.getnframes()))
        if channels == 1:
            stereo = array('h',[0])*(len(pcm)*2)
            stereo[0::2] = pcm;stereo[1::2] = pcm
            pcm = stereo
        else:
            assert channels == 2
        assert clip['clip_in'] == 0 and clip['time_scale'] == 1, clip
        start = round(clip['start']*48000)
        count = min(len(pcm)//2, round(clip['duration']*48000), max(0,frames-start))
        if not clip['effectively_muted'] and count:
            segments.append((start,start+count,pcm[:count*2].tobytes()))
        cues.append({**clip,'en':locale[clip['key']]['en'],'ru':locale[clip['key']]['ru'],'audio':target.relative_to(directory).as_posix(),'original_audio':cue['english_audio'],'characters':cue['character_ids'],'reference_frames':count})
    boundaries = sorted([(a,1) for a,b,p in segments]+[(b,-1) for a,b,p in segments],key=lambda x:(x[0],x[1]))
    current = maximum = 0
    for _,change in boundaries:
        current += change;maximum = max(current,maximum)
    gain = 1/max(1,maximum)
    mixed = bytearray(frames*4)
    for start,end,pcm in segments:
        if gain != 1:
            pcm = audioop.mul(pcm,2,gain)
        mixed[start*4:end*4] = audioop.add(bytes(mixed[start*4:end*4]),pcm,2)
    with wave.open(str(directory/'audio/voice_timeline.wav'),'wb') as sound:
        sound.setparams((2,2,48000,0,'NONE','not compressed'));sound.writeframes(mixed)
    active = [c for c in cues if not c['effectively_muted']]
    for language in ('ru','en'):
        (directory/f'subtitles.{language}.srt').write_text('\n\n'.join(f"{i}\n{srt_time(c['start'])} --> {srt_time(min(c['start']+c['duration'],scene['duration_seconds']))}\n{c[language]}" for i,c in enumerate(active,1))+'\n',encoding='utf8')
    return cues, {'reference':'audio/voice_timeline.wav','sample_rate':48000,'channels':2,'seconds':frames/48000,'maximum_simultaneous_voices':maximum,'reference_gain':gain,'note':'Voice reference only. Original start times; clip-duration trimming; equal fixed headroom if voices overlap. Original WAV stems remain unchanged. Music/ambience are separate.'}


def stems(directory, scene, archive, events, media):
    result = []
    for reference in scene['controller_events']:
        info = dict(reference)
        if not reference['event_id']:
            result.append({**info,'status':'no_event_assigned_in_source','media':[]});continue
        event = events[str(reference['event_id'])]
        info['wwise_event_xml'] = ET.tostring(event,encoding='unicode')
        info['media'] = []
        for mid in sorted({p.attrib['Id'] for p in event.iter('MediaRef')}):
            assert mid in media, (reference,mid)
            source = media[mid]
            member = 'assets/Audio/GeneratedSoundBanks/Windows/'+source.findtext('Path').replace('\\','/')
            data = archive.read(member)
            wem = directory/f'audio/{reference["event"]}_{mid}.wem'
            wem.parent.mkdir(parents=True,exist_ok=True)
            changed = not wem.exists() or wem.read_bytes() != data
            if changed:
                wem.write_bytes(data)
            wav = wem.with_suffix('.wav')
            if changed or not wav.exists():
                subprocess.run([str(ROOT/'local/vgmstream/vgmstream-cli.exe'),'-i','-o',str(wav),str(wem)],capture_output=True,check=True)
            with wave.open(str(wav),'rb') as sound:
                props = {'seconds':sound.getnframes()/sound.getframerate(),'channels':sound.getnchannels(),'sample_rate':sound.getframerate(),'sample_width':sound.getsampwidth()}
            info['media'].append({'id':mid,'short_name':source.findtext('ShortName'),'language':source.attrib.get('Language'),'quest_member':member,'wem':wem.relative_to(directory).as_posix(),'wav':wav.relative_to(directory).as_posix(),**props})
        info['status'] = 'original_media_extracted_and_decoded'
        result.append(info)
    return result


def seal(directory):
    files = sorted(p for p in directory.rglob('*') if p.is_file() and p.name != 'SHA256SUMS.txt')
    (directory/'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(directory).as_posix()}\n' for p in files),encoding='utf8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--include-prologue',action='store_true')
    args = parser.parse_args()
    graph, scenes = scan_scenes()
    dialogue = {r['key']:r for r in json.loads((ROOT/'campaign-export/manifests/dialogue.json').read_text(encoding='utf8'))}
    locale = json.loads((ROOT/'campaign-export/manifests/localization.json').read_text(encoding='utf8'))
    soundroot = ET.parse(GAME/'StreamingAssets/Audio/GeneratedSoundBanks/Windows/SoundbanksInfo.xml').getroot()
    events = {e.attrib['Id']:e for e in soundroot.iter('Event')}
    media = {f.attrib['Id']:f for f in soundroot.iter('File') if f.attrib.get('Language') == 'SFX'}
    pictures = Images()
    index = []
    with zipfile.ZipFile(next(QUEST.rglob('*.obb'))) as archive:
        for scene in scenes:
            if scene['mission'] == 'Mission_T1' and not args.include_prologue:
                path = OUT/'prologue'
                manifest = json.loads((path/'manifest.json').read_text(encoding='utf8'))
                index.append({'mission':scene['mission'],'field':scene['field'],'directory':'prologue','duration_seconds':scene['duration_seconds'],'voice_cues':len(manifest['dialogue_cues']),'images':len(manifest['images']),'controller_media':len(manifest['stems']),'status':manifest['status']})
                continue
            suffix = 'intro' if scene['field'] == '_introScene' else 'outro'
            directory = OUT/f'{scene["mission"]}_{suffix}'
            directory.mkdir(parents=True,exist_ok=True)
            print(f'Preparing {directory.name}',flush=True)
            save_json(directory/'source/timeline.json',scene)
            save_json(directory/'source/scene-audit.json',list(graph.rows(scene['scene_source']).values()))
            for source in {scene['root']['source'],scene['nominal_asset_source']}:
                save_json(directory/f'source/{source}.json',list(graph.rows(source).values()))
            images = pictures.extract(graph,scene,directory)
            contact_sheet(directory,images)
            cues, voice = voices(directory,scene,dialogue,locale)
            soundtrack = stems(directory,scene,archive,events,media)
            status = 'source_components_extracted; no_flattened_video; not_installed; not_engine_tested'
            manifest = {'mission':scene['mission'],'field':scene['field'],'scene':scene['scene'],'version':'Quest 1.1.0-16520','duration_seconds':scene['duration_seconds'],'timeline_root':scene['root'],'dialogue_cues':cues,'images':images,'stems':soundtrack,'voice_reference':voice,'status':status,'notes':['Music and ambience are original separate stems, without reconstruction of Wwise bus gains or scene-transition offsets.','Cube faces follow Unity order, decoded without vertical flip; final camera/projection needs review.','Animated 3D staging, nested directors, fades and the final flattened video still need rendering/adaptation.','All documentary sources and reviewed RU remain in the project; source English and legacy RAW translation are unchanged.']}
            save_json(directory/'manifest.json',manifest)
            body = f'# {scene["mission"]} — {suffix}\n\nДлительность таймлайна: {scene["duration_seconds"]:.6f} с. Источник: Quest 1.1.0-16520.\n\nПодготовлены {len(images)} изображений, {len(cues)} речевых клипов, оригинальные WEM/WAV музыки/окружения, EN/RU SRT, голосовой референс и разобранные данные сцены/таймлайна.\n\nСм. manifest.json, source-contact.jpg и source/. В audio/voice_timeline.wav только голос; музыка и окружение лежат отдельными дорожками. В финале отсутствие ambience-event отражает исходную привязку.\n\nЭто исходники для сборки ролика. Готовый WebM/NIS не создавался, в игру ничего не устанавливалось.\n'
            (directory/'README.md').write_text(body,encoding='utf8')
            seal(directory)
            index.append({'mission':scene['mission'],'field':scene['field'],'directory':directory.name,'duration_seconds':scene['duration_seconds'],'voice_cues':sum(not c['effectively_muted'] for c in cues),'images':len(images),'controller_media':sum(len(s['media']) for s in soundtrack),'status':status})
            print(json.dumps(index[-1],ensure_ascii=False),flush=True)
    save_json(ROOT/'campaign-export/manifests/timelines.json',timeline_manifest(scenes))
    save_json(OUT/'index.json',{'source_version':'Quest 1.1.0-16520','scenes':index,'notes':['M7 and M9 share sharedassets30.assets but use different TimelineAssets. Resolve through the scene PlayableDirector.','M1 uses the shared prologue now placed before T1; no second package or second playback is needed.','Source preparation only; videos, final audio mixing and engine integration remain pending.']})
    lines = ['# Ролики HWVR — подготовка к переносу','', 'Подготовлены **12 исходных сцен**: общий пролог, десять других вступлений и финал. Здесь указан состав исходников; актуальное состояние видео и установки — [подключение роликов](CAMPAIGN_SPEECH.md).','',
        'Для каждой сцены: оригинальные изображения, речевые WAV, музыка/окружение WEM и WAV, новый RU и EN SRT, голосовой референс по исходным таймингам, сценические привязки, материалы панорам, переходы/сигналы и SHA256. У общего пролога сохранён прежний формат пакета.','',
        '| Сцена | Длительность | Реплик | Изображений | Файлов музыки/окружения | Пакет |','|---|---:|---:|---:|---:|---|']
    for row in index:
        name = row['mission'].removeprefix('Mission_')+' — '+('финал' if row['field']=='_outroScene' else 'вступление')
        path = (OUT/row['directory']/'manifest.json').as_posix()
        seconds = row['duration_seconds'];time = f'{int(seconds//60)}:{seconds%60:06.3f}'
        lines.append(f'| {name} | {time} | {row["voice_cues"]} | {row["images"]} | {row["controller_media"]} | [Состав](<{path}>) |')
    lines += ['', '**Исправлена принадлежность реплик:** сцены M7 и M9 используют один sharedassets30.assets. Ранее 35 клипов попадали в M7, а M9 получала пустой список. Теперь по привязке PlayableDirector разделены 15 клипов M7 и 20 клипов M9. Общее число 125 клипов не изменилось; изменилось распределение по главам.','',
        'Четырёхканальное окружение оставлено в исходном виде. Громкости Wwise и момент старта звука относительно перехода сцены пока не восстановлены. Голосовой референс не включает музыку; при наложении голосов фиксированное уменьшение уровня отмечено в manifest.json. Исходные отдельные WAV не изменяются.','',
        'В M13-финале ambience-event не задан: это сохранённая исходная конфигурация. Отсутствующую дорожку не заменяли другой. Панорамы и портреты не воспроизводят сами по себе движение кораблей: 3D-постановка, проекция, переходы и финальное сведение ещё требуют работы.','',
        'Связь с HWRM: [план подключения перед T1](reference/PROLOGUE_SOURCES.md). Остальные вступления подключать к соответствующей главе через postload, финал — при успешном окончании M13. Актуальное подключение и ограничения — [отчёт об интеграции](CAMPAIGN_SPEECH.md).','',
        'Воспроизведение подготовки: `.venv\\Scripts\\python.exe -X utf8 tools\\prepare_campaign_cinematics.py`. Общая сводка — `campaign-export/cinematics/index.json`. Для повторного включения общего пролога в новый формат есть `--include-prologue`; существующий пакет prologue по умолчанию сохраняется.','']
    (ROOT/'docs/CAMPAIGN_CINEMATICS.md').write_text('\n'.join(lines),encoding='utf8')
    print(json.dumps({'scenes':len(index),'voice_cues':sum(r['voice_cues'] for r in index),'images':sum(r['images'] for r in index),'controller_media':sum(r['controller_media'] for r in index)},ensure_ascii=False),flush=True)


if __name__ == '__main__':
    main()
