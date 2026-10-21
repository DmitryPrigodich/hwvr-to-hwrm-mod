"""Use stock Kushan portraits for Novokushan ships with direct visual counterparts."""

import json
import re
from pathlib import Path

from gallery_layout import FACTIONS

ICON_MAPPING={ident:native for _,pairs in FACTIONS[0][1] for ident,native in pairs
              if native and native.startswith('kus_') and ident.startswith('nku_')}

def prepare(destination):
    source=Path('local/hwrm-base/ship/icons/shipicons.lua')
    text=source.read_text(encoding='utf-8-sig')
    available={name.lower():name for name in re.findall(r'(?m)^([A-Za-z_0-9]+)\s*=\s*\{',text)}
    mapping=ICON_MAPPING
    aliases=[]
    for ident,native in mapping.items():
        if native not in available:raise ValueError('Missing original ship icon: '+native)
        aliases.append(f'{ident} = {available[native]}')
    text+='\n-- Novokushan portraits: original Kushan atlas entries.\n'+'\n'.join(aliases)+'\n'
    folder=destination/'ship/icons';folder.mkdir(parents=True,exist_ok=True)
    (folder/'shipicons.lua').write_text(text,encoding='utf-8')
    report=dict(aliases=mapping,count=len(mapping),source=str(source),radaa_changed=False,
                texture='DATA:\\Ship\\Icons\\HW1_icon_Kus_ships.dds')
    (destination/'ship-icons-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    Path('local/ship-icons-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Prepared {len(mapping)} Kushan portrait aliases for Novokushan hulls')
    return report
