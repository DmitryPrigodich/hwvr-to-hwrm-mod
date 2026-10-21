"""Resolve each cinematic through its scene controller, not its asset filename.

Unity can store more than one scene's TimelineAsset in the same sharedassets file.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SourceGraph:
    def __init__(self):
        self.raw = ROOT/'local/quest-audit'
        self.metadata = json.loads((self.raw/'index.json').read_text(encoding='utf8'))
        self.cache = {}
        self.built = json.loads((ROOT/'local/quest-campaign/summary.json').read_text(encoding='utf8'))['built_scenes']

    def rows(self, source):
        if source not in self.cache:
            self.cache[source] = {r['path_id']: r for r in json.loads((self.raw/(source+'.json')).read_text(encoding='utf8'))}
        return self.cache[source]

    def address(self, source, pointer):
        if not pointer or not pointer.get('m_PathID'):
            return None
        target = source if not pointer.get('m_FileID') else self.metadata['files'][source]['externals'][pointer['m_FileID']-1]
        return target, pointer['m_PathID']

    def deref(self, source, pointer):
        address = self.address(source, pointer)
        return self.rows(address[0]).get(address[1]) if address else None

    def scene(self, entry):
        number = self.built.index(entry['scene'])
        scene_source = f'level{number}'
        rows = self.rows(scene_source)
        controllers = [r for r in rows.values() if r['class_name'] == 'Hercules.TimelineController']
        assert len(controllers) == 1, (scene_source, len(controllers))
        controller = controllers[0]
        directors = [r for r in rows.values() if r['class_name'] == 'PlayableDirector' and r['data']['m_GameObject'] == controller['data']['m_GameObject']]
        assert len(directors) == 1, scene_source
        director = directors[0]
        root = self.deref(scene_source, director['data']['m_PlayableAsset'])
        assert root['class_name'] == 'UnityEngine.Timeline.TimelineAsset'
        tracks = []
        seen = set()

        def walk(owner, pointer, parent_muted=False):
            row = self.deref(owner, pointer)
            identity = row['source'], row['path_id']
            assert identity not in seen, identity
            seen.add(identity)
            muted = bool(parent_muted or row['data'].get('m_Muted'))
            tracks.append({'source': row['source'], 'path_id': row['path_id'], 'class_name': row['class_name'], 'name': row['data'].get('m_Name'), 'effectively_muted': muted, 'data': row['data']})
            for child in row['data'].get('m_Children', []):
                walk(row['source'], child, muted)

        for pointer in root['data']['m_Tracks']:
            walk(root['source'], pointer)
        if root['data'].get('m_MarkerTrack', {}).get('m_PathID'):
            walk(root['source'], root['data']['m_MarkerTrack'])

        receiver_signals = set()
        for receiver in rows.values():
            if receiver['class_name'] != 'UnityEngine.Timeline.SignalReceiver':
                continue
            events = receiver['data']['m_Events']
            for signal, event in zip(events['m_Signals'], events['m_Events'], strict=True):
                for call in event.get('m_PersistentCalls', {}).get('m_Calls', []):
                    if call.get('m_MethodName') == 'EndCutsceneFromTimeline' and self.address(scene_source, call['m_Target']) == (scene_source, controller['path_id']):
                        receiver_signals.add(self.address(scene_source, signal))

        cues = []
        signals = []
        visual_clips = []
        assets = {}
        for track in tracks:
            source = track['source']
            for marker in track['data'].get('m_Markers', {}).get('m_Objects', []):
                row = self.deref(source, marker)
                if row and row['class_name'] == 'UnityEngine.Timeline.SignalEmitter':
                    end = self.address(row['source'], row['data']['m_Asset']) in receiver_signals
                    signals.append({'time': row['data']['m_Time'], 'ends_cutscene': end, 'effectively_muted': track['effectively_muted'], 'source': row['source'], 'path_id': row['path_id'], 'track': track['path_id']})
                    assets[row['source'], row['path_id']] = row
            for clip in track['data'].get('m_Clips', []):
                row = self.deref(source, clip.get('m_Asset'))
                if not row:
                    continue
                assets[row['source'], row['path_id']] = row
                common = {'start': clip['m_Start'], 'duration': clip['m_Duration'], 'clip_in': clip.get('m_ClipIn', 0), 'time_scale': clip.get('m_TimeScale', 1), 'effectively_muted': track['effectively_muted'], 'track_source': source, 'track': track['path_id'], 'asset_source': row['source'], 'asset_path_id': row['path_id']}
                if row['class_name'] == 'Hercules.DialogueAudioAsset':
                    line = self.deref(row['source'], row['data']['Data']['DialogueLine'])
                    cues.append({**common, 'key': line['data']['_textKey'], 'source': line['source'], 'path_id': line['path_id']})
                    assets[line['source'], line['path_id']] = line
                elif row['class_name'] in ('Hercules.BillboardAsset', 'Hercules.SkyboxControlAsset', 'Hercules.CameraFadeAsset'):
                    visual_clips.append({**common, 'class_name': row['class_name'], 'data': row['data']['Data']})
        end_times = [s['time'] for s in signals if s['ends_cutscene'] and not s['effectively_muted']]
        assert len(end_times) == 1, (entry['scene'], signals)
        cues.sort(key=lambda c: (c['start'], c['key']))
        events = []
        for field in ('_musicEvent', '_ambienceEvent'):
            ref = controller['data'].get(field, {}).get('WwiseObjectReference')
            row = self.deref(scene_source, ref)
            events.append({'role': field, 'reference': ref, 'event': row['data']['objectName'] if row else None, 'event_id': row['data']['id'] if row else None})
            if row:
                assets[row['source'], row['path_id']] = row
        return {'mission': entry['mission'], 'field': entry['field'], 'scene': entry['scene'], 'scene_source': scene_source, 'nominal_asset_source': f'sharedassets{number}.assets', 'root': {'source': root['source'], 'path_id': root['path_id'], 'data': root['data']}, 'controller': controller, 'director': director, 'tracks': tracks, 'signals': signals, 'duration_seconds': end_times[0], 'clips': cues, 'visual_clips': visual_clips, 'controller_events': events, 'resolved_records': list(assets.values())}


def scan_scenes():
    graph = SourceGraph()
    missions = json.loads((ROOT/'local/quest-campaign/missions.json').read_text(encoding='utf8'))
    missions = [m for m in missions if m['category']=='_tutorialMissions']+[m for m in missions if m['category']=='_campaignMissions']
    entries = []
    seen = set()
    for mission in missions:
        definition = graph.rows(mission['source'])[mission['path_id']]
        for field in ('_introScene','_outroScene'):
            scene = definition['data'].get(field,{}).get('_path')
            if not scene or scene in seen or scene not in graph.built:
                continue
            seen.add(scene)
            entries.append({'mission':mission['id'],'field':field,'scene':scene})
    return graph, [graph.scene(entry) for entry in entries]


def timeline_manifest(scenes):
    return [{'mission': scene['mission'], 'field': scene['field'], 'scene': scene['scene'], 'source': scene['nominal_asset_source'], 'timeline_source': scene['root']['source'], 'timeline_path_id': scene['root']['path_id'], 'duration_seconds': scene['duration_seconds'], 'clips': [c for c in scene['clips'] if not c['effectively_muted']], 'muted_clips': [c for c in scene['clips'] if c['effectively_muted']], 'status': 'scene_controller_timeline_resolved; source_components_extracted_separately; camera_and_animation_need_NIS_or_video_conversion'} for scene in scenes]


if __name__ == '__main__':
    _, scenes = scan_scenes()
    for scene in scenes:
        print(json.dumps({k: scene[k] for k in ('mission','field','duration_seconds')} | {'root': [scene['root']['source'],scene['root']['path_id']], 'cues': len(scene['clips']), 'events': scene['controller_events']}, ensure_ascii=False))
