"""Copy the current generated fleet code into a versioned, asset-free snapshot.

The live generator output remains local/fleet-preview/source. This snapshot
keeps the exact released definitions reviewable without committing game assets.
"""
import hashlib
import json
import shutil
from pathlib import Path
from build_minicampaign import runtime_file

PROJECT=Path(__file__).resolve().parents[1]
SOURCE=PROJECT/'local/fleet-preview/source'
TARGET=PROJECT/'fleet-preview'
TEXT_EXTENSIONS={'.lua','.ship','.wepn','.subs','.events','.level','.campaign','.ucs'}


def snapshot():
    source=SOURCE
    speech=PROJECT/'local/campaign-speech/integration.json'
    if speech.exists() and json.loads(speech.read_text(encoding='utf8')).get('enabled') is True:
        source=(PROJECT/'local/campaign-speech/source').resolve()
    assert source.resolve().is_relative_to((PROJECT/'local').resolve())
    source_root=source
    files={p.relative_to(source).as_posix():p for p in source.rglob('*') if p.is_file() and runtime_file(p,source) and p.suffix.lower() in TEXT_EXTENSIONS}
    assert files and (source/'preview-id.txt').read_text().strip()=='VRC-two-faction-no-research-preview-v1'
    manifest=TARGET/'snapshot.json'
    previous=json.loads(manifest.read_text(encoding='utf8')) if manifest.exists() else None
    if previous:
        assert previous['identity']=='VRC-fleet-code-snapshot-v1'
        for name in previous['files']:
            path=(TARGET/name).resolve()
            assert path.is_relative_to(TARGET.resolve())
            if name not in files and path.exists():path.unlink()
    hashes={}
    for name,source in sorted(files.items()):
        text=source.read_text(encoding='utf-16' if source.suffix=='.ucs' else 'ascii')
        destination=TARGET/name
        destination.parent.mkdir(parents=True,exist_ok=True)
        if source.suffix=='.ucs':shutil.copy2(source,destination)
        else:destination.write_text(text,encoding='ascii',newline='\n')
        hashes[name]=hashlib.sha256(destination.read_bytes()).hexdigest()
    manifest.write_text(json.dumps({'identity':'VRC-fleet-code-snapshot-v1','source':source_root.relative_to(PROJECT).as_posix(),'files':hashes},indent=2)+'\n',encoding='utf8')
    print(json.dumps({'snapshot':str(TARGET),'text_files':len(hashes),'game_assets_copied':0}))


if __name__=='__main__':snapshot()
