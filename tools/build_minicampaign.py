"""Package the script-only mini-campaign with the official Steam toolkit."""
import hashlib
import json
import subprocess
import struct
from pathlib import Path
from launch_game import short_path

PROJECT=Path(__file__).resolve().parent.parent
TOOL=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Homeworld 347380\GBXTools\WorkshopTool\Archive.exe")
ROOT=PROJECT/'minicampaign'
OUTPUT=PROJECT/'local/VastReachesMiniCampaign.big'


def native_aliases(path):
    with path.open('rb') as f:
        header=f.read(180)
        if header[:12]!=b'_ARCHIVE\x02\0\0\0':raise RuntimeError('Unexpected BIG format.')
        metadata_size=struct.unpack_from('<I',header,172)[0]
        if not 24<=metadata_size<16*1024*1024:raise RuntimeError('Invalid BIG metadata size.')
        metadata=f.read(metadata_size)
    offset,count=struct.unpack_from('<IH',metadata)
    if offset+138*count>len(metadata):raise RuntimeError('Invalid BIG TOC table.')
    aliases=[metadata[offset+i*138:offset+i*138+64].split(b'\0')[0].decode('ascii') for i in range(count)]
    if any(alias not in ('data','locale') for alias in aliases):
        raise RuntimeError('Unsupported native TOC alias: '+repr(aliases)+'. Package languages as sibling BIG files.')
    return aliases


def archive(manifest, output):
    for label,cmd in [('build',[str(TOOL),'-c',str(manifest),'-r',short_path(ROOT)+'\\','-a',str(output)]),('test',[str(TOOL),'-a',str(output),'-t'])]:
        proc=subprocess.run(cmd,capture_output=True,text=True)
        log=proc.stdout+proc.stderr
        output.with_suffix('.'+label+'.log').write_text(log,encoding='utf8')
        if proc.returncode or any(word in log for word in ('Error','ERROR','Failed','Could not')):
            raise RuntimeError(label+': '+log)
        if label=='test' and 'TEST: PASSED' not in log:
            raise RuntimeError('Archive test did not confirm success: '+log)
    native_aliases(output)


def localized_files(language):
    return sorted(p for p in (ROOT/f'locale/{language}').rglob('*') if p.is_file() and not (p.parent.name.lower()=='animatics' and p.name.lower().startswith('vre_')))


def locale_toc(language, name, short):
    # The native alias is "locale". Languages are selected by loading sibling
    # English.big / Russian.big, as documented by the shipped WorkshopTool.
    return [f'TOCStart name="{name}" alias="locale" relativeroot="locale\\{language}"',
            'FileSettingsStart defcompression="2"','FileSettingsEnd',
            *[short+'\\'+str(p.relative_to(ROOT)) for p in localized_files(language)],'TOCEnd']


def build():
    short=short_path(ROOT)
    files=[p for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name not in ('cinematic-update-id.txt','campaign-speech-id.txt') and not (p.relative_to(ROOT).parts[0]=='locale' and len(p.relative_to(ROOT).parts)>2)]
    lines=['Archive name="Vast Reaches mini campaign"','TOCStart name="VRCMiniData" alias="data" relativeroot=""','FileSettingsStart defcompression="2"','FileSettingsEnd']
    lines += [short+'\\'+str(p.relative_to(ROOT)) for p in files]
    lines += ['TOCEnd']
    # Retain one English fallback in the main BIG; a selected sibling locale
    # archive overrides it. Do not invent colon-qualified TOC aliases.
    lines += locale_toc('English','VRCMiniLocale',short)
    lines += ['']
    manifest=OUTPUT.with_suffix('.archive.txt')
    manifest.write_text('\r\n'.join(lines),encoding='ascii',newline='')
    archive(manifest,OUTPUT)
    assert OUTPUT.is_file() and OUTPUT.stat().st_size>3000
    language_archives=[]
    for language in ('English','Russian'):
        output=OUTPUT.parent/(language+'.big')
        localized_manifest=output.with_suffix('.archive.txt')
        localized_manifest.write_text('\r\n'.join(['Archive name="Vast Reaches '+language+'"',*locale_toc(language,'VRCMini'+language,short),'']),encoding='ascii',newline='')
        archive(localized_manifest,output)
        language_archives.append({'language':language,'archive':str(output),'size':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()})
    result={'archive':str(OUTPUT),'size':OUTPUT.stat().st_size,'sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),'source_files':len(files)+len(localized_files('English')),'locales':['Russian','English'],'locale_fallback':'English','language_archives':language_archives,'game_launched':False}
    (PROJECT/'local/minicampaign-build.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    build()
