"""Validate native speech resources and blocked/serial subtitle flow without HWRM."""
import json
import re
import subprocess
import wave
from pathlib import Path
from lupa.lua51 import LuaRuntime
from PIL import Image
import campaign_speech as speech
import verify_minicampaign as mini


def verify(scripts_only=False):
    report=json.loads((speech.WORK/'integration.json').read_text(encoding='utf8'))
    source=Path(report['source'])
    training={row['key'] for row in report['mission_lines'] if row['key'].startswith('T01_')}
    assert len(training)==37 and 'T01_070_060_TS' in training and 'T01_030_020_FI' not in training
    for line in report['mission_lines']:
        path=source/line['path']
        with wave.open(str(path)) as w:
            assert (w.getnchannels(),w.getframerate(),w.getsampwidth())==(1,44100,2)
            assert abs(w.getnframes()/44100-line['duration'])<.001
        assert path.stem==line['text'][1:]
        vm=LuaRuntime();vm.execute(path.with_suffix('.lua').read_text());assert vm.globals().version==4 and vm.globals().compression==0
    themes={};vm=LuaRuntime();vm.globals().addTheme=lambda *args:themes.__setitem__(args[0],args)
    vm.globals().addRegion=lambda *args:None
    vm.execute((source/'ui/subtitle.lua').read_text())
    original={};vm=LuaRuntime();vm.globals().addTheme=lambda *args:original.__setitem__(args[0],args)
    vm.globals().addRegion=lambda *args:None
    vm.execute((speech.ROOT/'local/hwrm-base/ui/subtitle.lua').read_text())
    for i in range(27):
        assert themes[i][2:]==original[i][2:],i
    for actor in range(27,32):
        name=themes[actor][5].replace('#','0')
        assert Image.open(source/'ui/speechicons'/name).size==(384,192)
    movie_cues=len(report['animatic_cues'])
    assert report['animatic_audio_mode']=='movie_owned'
    for row in report['movie_audio']:
        path=source/row['path'];assert speech.sha(path)==row['sha256']
        with wave.open(str(path)) as w:
            assert (w.getnchannels(),w.getframerate(),w.getsampwidth())==(1,44100,2)
            assert abs(w.getnframes()/44100-row['duration'])<.001
        for language in ('English','Russian'):
            vm=LuaRuntime();vm.execute((source/f'locale/{language}/{row["movie"]}.lua').read_text())
            screen=vm.globals().MovieScreen
            assert screen.speechFilename is None,'Movie must not create narration events that survive skipping'
            assert screen[1].filenameA=='data:'+row['path'].removesuffix('.wav')
    from build_minicampaign import runtime_file
    assert not runtime_file(source/'sound/speech/animatic/VRC/VRE_Prologue/legacy.wav',source)
    assert not runtime_file(source/'locale/English/VRE_Prologue_speech.lua',source)
    mini.ROOT=source;mini.BASE=source/'leveldata/campaign/VastReachesMiniCampaign';mini.tests()
    e=mini.Engine('T01_Training')
    for _ in range(180):
        e.g.VRC_Tick()
        if e.g.VRC_ActiveActor is not None:break
    actor=e.g.VRC_ActiveActor;assert actor==27
    queue_index=e.g.VRC_QueueIndex
    e.subtitle_until[actor]=e.g.VRC_Time+80
    e.tick(35)
    assert e.g.VRC_QueueIndex==queue_index and e.g.VRC_IntroLock==1,'Busy native speech must block following dialogue/exercise'
    e.tick(55)
    assert e.g.VRC_QueueIndex>queue_index,'Queue must resume when native subtitle finishes'
    for row in report['movies']:
        path=speech.MOVIES/row['path'];assert speech.sha(path)==row['sha256'] and row['narration_embedded'] is False
        if not scripts_only:
            run=subprocess.run([str(speech.FFMPEG),'-v','error','-threads','1','-i',str(path),'-f','null','-'],capture_output=True,text=True)
            assert run.returncode==0 and not run.stderr,(path,run.stderr)
    result={'status':'passed','mission_lines':len(report['mission_lines']),'source_animatic_cues':movie_cues,'movie_owned_narration_tracks':len(report['movie_audio']),'music_only_movies_decoded':0 if scripts_only else len(report['movies']),'movie_hashes_verified':len(report['movies']),'native_busy_queue_test':'passed','stock_actor_themes_preserved':27,'engine_tested':False,'skip_stops_external_audio_native_test':'pending'}
    speech.save(speech.WORK/('verification-scripts.json' if scripts_only else 'verification.json'),result);print(json.dumps(result))


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--scripts-only',action='store_true')
    verify(scripts_only=parser.parse_args().scripts_only)
