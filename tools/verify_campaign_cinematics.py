"""Verify extracted cinematic packages against source references and media."""
import hashlib
import json
import re
import wave
import zipfile
from pathlib import Path

from PIL import Image

from campaign_cinematic_sources import ROOT, scan_scenes
from prepare_campaign_cinematics import OUT, QUEST
from prepare_intro_sources import save_json


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    graph, scenes = scan_scenes()
    source = {(s['mission'],s['field']):s for s in scenes}
    index = json.loads((OUT/'index.json').read_text(encoding='utf8'))
    assert len(index['scenes']) == len(source) == 12
    locale = json.loads((ROOT/'campaign-export/manifests/localization.json').read_text(encoding='utf8'))
    dialogue = {r['key']:r for r in json.loads((ROOT/'campaign-export/manifests/dialogue.json').read_text(encoding='utf8'))}
    timelines = json.loads((ROOT/'campaign-export/manifests/timelines.json').read_text(encoding='utf8'))
    assert {t['mission']:len(t['clips']) for t in timelines if t['field']=='_introScene'}['Mission_M7'] == 15
    assert {t['mission']:len(t['clips']) for t in timelines if t['field']=='_introScene'}['Mission_M9'] == 20
    results = []
    with zipfile.ZipFile(next(QUEST.rglob('*.obb'))) as archive:
        for entry in index['scenes']:
            directory = OUT/entry['directory']
            manifest = json.loads((directory/'manifest.json').read_text(encoding='utf8'))
            expected = source[entry['mission'],entry['field']]
            assert manifest['duration_seconds'] == expected['duration_seconds']
            hashes = {}
            for line in (directory/'SHA256SUMS.txt').read_text(encoding='utf8').splitlines():
                digest,name = line.split('  ',1)
                path = directory/name
                assert path.resolve().is_relative_to(directory.resolve())
                assert sha(path) == digest, path
                hashes[name] = digest
            assert set(hashes) == {p.relative_to(directory).as_posix() for p in directory.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt'}
            faces = {}
            for image in manifest['images']:
                with Image.open(directory/image['path']) as png:
                    assert list(png.size) == image['size']
                    png.verify()
                if 'face' in image:
                    faces.setdefault((image['source'],image['path_id']),[]).append(image['face'])
            assert all(len(f)==6 and len(set(f))==6 for f in faces.values())
            active = [c for c in manifest['dialogue_cues'] if not c.get('effectively_muted')]
            assert [(c['start'],c['key']) for c in active] == [(c['start'],c['key']) for c in expected['clips'] if not c['effectively_muted']]
            for cue in manifest['dialogue_cues']:
                assert cue['en'] == locale[cue['key']]['en'] and cue['ru'] == locale[cue['key']]['ru']
                origin = ROOT/'campaign-export'/dialogue[cue['key']]['english_audio']['wav']
                assert sha(directory/cue['audio']) == sha(origin)
            prefix = 'prologue' if entry['directory']=='prologue' else 'subtitles'
            for language in ('en','ru'):
                captions = (directory/f'{prefix}.{language}.srt').read_text(encoding='utf8').strip().split('\n\n')
                assert len(captions) == len(active)
                for block,cue in zip(captions,active,strict=True):
                    assert '\n'.join(block.splitlines()[2:]) == cue[language]
            media = []
            for stem in manifest['stems']:
                media.extend(stem.get('media',[]) if 'media' in stem else [stem])
            for item in media:
                member = item.get('quest_member')
                assert (directory/item['wem']).read_bytes() == archive.read(member)
                with wave.open(str(directory/item['wav']),'rb') as wav:
                    assert wav.getnchannels() == item['channels']
                    assert wav.getframerate() == item['sample_rate']
                    assert wav.getsampwidth() == item['sample_width']
                    assert abs(wav.getnframes()/wav.getframerate()-item['seconds']) < 1e-8
            voice = directory/('audio/prologue_voice_timeline.wav' if entry['directory']=='prologue' else manifest['voice_reference']['reference'])
            with wave.open(str(voice),'rb') as wav:
                assert wav.getnchannels()==2 and wav.getsampwidth()==2 and wav.getframerate()==48000
                assert abs(wav.getnframes()/wav.getframerate()-expected['duration_seconds']) <= 1/48000
            results.append({'package':entry['directory'],'files':len(hashes),'images':len(manifest['images']),'dialogue_cues':len(active),'controller_media':len(media),'cubemaps':len(faces)})
    docs = (ROOT/'docs/QUEST_SCENARIOS.md').read_text(encoding='utf8')
    # Source intro rows are in their respective chapter sections, after the corrected scan.
    m7 = next(t for t in timelines if t['mission']=='Mission_M7')
    m9 = next(t for t in timelines if t['mission']=='Mission_M9')
    assert not ({c['key'] for c in m7['clips']} & {c['key'] for c in m9['clips']})
    assert all(c['key'] in docs for c in m7['clips']+m9['clips'])
    sections = re.split(r'(?m)^## ',docs)
    m7_section = next(s for s in sections if s.startswith('2. M7:'))
    m9_section = next(s for s in sections if s.startswith('7. M9:'))
    assert all(c['key'] in m7_section and c['key'] not in m9_section for c in m7['clips'])
    assert all(c['key'] in m9_section and c['key'] not in m7_section for c in m9['clips'])
    for name in ('campaign_cinematic_sources','prepare_campaign_cinematics','verify_campaign_cinematics','prepare_campaign_media','write_quest_scenarios'):
        compile((ROOT/f'tools/{name}.py').read_text(encoding='utf8'),name,'exec')
    report = {'status':'passed','scenes':len(results),'files':sum(r['files'] for r in results),'images':sum(r['images'] for r in results),'dialogue_cues':sum(r['dialogue_cues'] for r in results),'controller_media':sum(r['controller_media'] for r in results),'package_results':results,'m7_m9_separation_verified':True,'video_rendered':False,'installed':False,'engine_tested':False}
    save_json(ROOT/'local/cinematic-preparation/verification.json',report)
    print(json.dumps(report,ensure_ascii=False))


if __name__ == '__main__':
    main()
