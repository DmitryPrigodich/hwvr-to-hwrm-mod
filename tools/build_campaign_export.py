"""Build and CRC-test the prepared campaign data with the official toolkit."""
import hashlib
import json
import subprocess
from pathlib import Path
from launch_game import short_path
import build_minicampaign as archives

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'campaign-export/data'
OUT=ROOT/'campaign-export/VastReachesCampaignPreparation.big'
TOOL=Path(r'C:\Program Files (x86)\Steam\steamapps\common\Homeworld 347380\GBXTools\WorkshopTool\Archive.exe')


def main():
    assert (DATA/'leveldata/campaign/VastReachesFull.campaign').is_file()
    short=short_path(DATA)
    files=[p for p in sorted(DATA.rglob('*')) if p.is_file() and archives.runtime_file(p,DATA) and not (p.relative_to(DATA).parts[0]=='locale' and len(p.relative_to(DATA).parts)>2)]
    toc=['Archive name="Vast Reaches Campaign Preparation"','TOCStart name="VREPrepData" alias="data" relativeroot=""','FileSettingsStart defcompression="2"','FileSettingsEnd']
    toc += [short+'\\'+str(p.relative_to(DATA)) for p in files]
    toc += ['TOCEnd']
    archives.ROOT=DATA
    toc += archives.locale_toc('English','VREPrepLocale',short)
    toc += ['']
    manifest=ROOT/'local/campaign-export.archive.txt'
    manifest.write_text('\r\n'.join(toc),encoding='ascii',newline='')
    reports=ROOT/'campaign-export/checks';reports.mkdir(exist_ok=True)
    for label,args in [('build',['-c',str(manifest),'-r',short+'\\','-a',str(OUT)]),('test',['-a',str(OUT),'-t'])]:
        run=subprocess.run([str(TOOL)]+args,capture_output=True,text=True)
        log=run.stdout+run.stderr;(reports/('archive-'+label+'.log')).write_text(log,encoding='utf8')
        if run.returncode or any(t in log for t in ('Error','ERROR','Failed','Could not')):raise RuntimeError(log[-2000:])
        if label=='test':assert 'TEST: PASSED' in log,log[-2000:]
    archives.native_aliases(OUT)
    language_archives=[]
    for language in ('English','Russian'):
        output=OUT.parent/(language+'.big')
        locale_manifest=ROOT/f'local/campaign-export-{language}.archive.txt'
        locale_manifest.write_text('\r\n'.join(['Archive name="VRE Preparation '+language+'"',*archives.locale_toc(language,'VREPrep'+language,short),'']),encoding='ascii',newline='')
        archives.archive(locale_manifest,output)
        language_archives.append({'language':language,'file':output.name,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()})
    result={'file':OUT.name,'bytes':OUT.stat().st_size,'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'files':len(files)+len(archives.localized_files('English')),'locales':['Russian','English'],'locale_fallback':'English','language_archives':language_archives,'russian_locale':True,'audio_in_archive':any(p.suffix=='.wav' for p in files),'loose_movies_required':True,'purpose':'Unplayed inspection/export build; not a complete playable campaign.','game_launched':False}
    (reports/'archive.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
