"""Resolve pinned source dependencies without importing their working copies as campaign code."""
import json
import os
from pathlib import Path
import subprocess
import sys

PROJECT=Path(__file__).resolve().parents[1]
RACES=PROJECT/'dependencies/hw1-races'
BASE=RACES/'dependencies/mp-patch'

def configure():
    settings=PROJECT/'local/mod-layer-settings.json'
    config=json.loads(settings.read_text(encoding='utf8')) if settings.exists() else {}
    os.environ.setdefault('HWRM_ASSET_CACHE',config.get('asset_cache',str(PROJECT/'local')))
    if not (BASE/'tools/hwrm_common.py').is_file():
        raise RuntimeError('Initialize dependencies with git submodule update --init --recursive.')
    sys.path.insert(0,str(BASE/'tools'))
    return config

def check_revision():
    lock=json.loads((PROJECT/'dependencies.lock.json').read_text(encoding='utf8'))
    head=subprocess.check_output(['git','-C',str(RACES),'rev-parse','HEAD'],text=True).strip()
    assert head==lock['hw1_races']['commit'],'Update the race dependency and lock explicitly.'
    return head
