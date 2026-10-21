"""Check texture identity, borrowed rig metadata, build entries and live gallery load."""

import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

from borrow_native_rig import chunks
from catalogue import native_folder
from fleet import FLEET
from source_weapon_mounts import read_hierarchy
from prepare_ship_icons import ICON_MAPPING


def textures(binary):
    hvmd=dict(chunks(binary))[b'HVMD']
    result={}
    for kind,chunk in chunks(hvmd,12):
        if kind==b'LMIP':
            length=struct.unpack_from('<I',chunk,8)[0]
            result[chunk[12:12+length].decode('ascii')]=chunk[12+length:16+length].decode('ascii')
    return result


def verify(live=False):
    stage=Path('local/testmod')
    catalogue=json.loads((stage/'catalogue-manifest.json').read_text(encoding='utf-8'))
    playable=json.loads((stage/'fleet-manifest.json').read_text(encoding='utf-8'))
    gallery=json.loads(Path('local/gallery-manifest.json').read_text(encoding='utf-8'))
    report=dict(models={},errors=[],playable_count=len(playable),catalogue_count=len(catalogue),gallery_count=len(gallery),visual_capture_verified=False)
    owners={}
    material_owners={}
    for spec in [*FLEET,*catalogue]:
        binary=(stage/'ship'/spec['id']/(spec['id']+'.hod')).read_bytes()
        maps=textures(binary)
        hvmd=dict(chunks(binary))[b'HVMD']
        for kind,chunk in chunks(hvmd,12):
            if kind==b'NRML' and chunk[8:12]==b'STAT':
                length=struct.unpack_from('<I',chunk,16)[0];name=chunk[20:20+length].decode('ascii')
                if name in material_owners:report['errors'].append(f'Material name collision: {name}')
                material_owners[name]=spec['id']
        for name,fmt in maps.items():
            if name in owners:report['errors'].append(f'Texture name collision: {name}: {owners[name]}, {spec["id"]}')
            owners[name]=spec['id']
            if name.startswith('hull_'):report['errors'].append(f'Non-unique legacy texture: {spec["id"]}/{name}')
            if fmt not in ('DXT1','DXT3','DXT5'):report['errors'].append(f'Uncompressed texture: {spec["id"]}/{name}/{fmt}')
        info=dict(texture_names=list(maps),formats=sorted(set(maps.values())),bytes=len(binary))
        if spec.get('buildable'):
            source=native_folder(spec['archetype'])/(spec['archetype']+'.hod')
            source_meta=dict(chunks(dict(chunks(source.read_bytes()))[b'DTRM'],12))
            target_meta=dict(chunks(dict(chunks(binary))[b'DTRM'],12))
            original_nodes=read_hierarchy(source_meta[b'HIER'])
            target_nodes=read_hierarchy(target_meta[b'HIER'])
            baseline=[node for node in target_nodes if not node['name'].startswith('Weapon_VR')]
            info['native_rig_matches']=(baseline==original_nodes and all(source_meta[k]==target_meta.get(k) for k in (b'DOCK',b'MRKS') if k in source_meta))
            if not info['native_rig_matches']:report['errors'].append(f'Incomplete borrowed rig: {spec["id"]}')
            if spec.get('source_weapon_mounts'):
                nodes={n['name']:n for n in target_nodes}
                ship_text=(stage/'ship'/spec['id']/(spec['id']+'.ship')).read_text()
                for mount in spec['source_weapon_mounts']['source_mounts']:
                    actual=nodes[mount['name']+'_Position']['values'][:3]
                    if max(abs(a-b) for a,b in zip(actual,mount['position']))>0.0001:
                        report['errors'].append('Misplaced source weapon mount: '+spec['id'])
                if any(line.startswith('StartShipHardPointConfig') and ',"Weapon",' in line for line in ship_text.splitlines()):
                    report['errors'].append('Foreign gun subsystem remains: '+spec['id'])
                info['source_weapon_mount_count']=len(spec['source_weapon_mounts']['source_mounts'])
        report['models'][spec['id']]=info
    for race in ('novokushan','radaa'):
        build=(stage/'scripts/races'/race/'scripts/def_build.lua').read_text()
        for ship in [s for s in playable if s['race']==race]:
            if f'ThingToBuild = "{ship["id"]}"' not in build:report['errors'].append(f'Missing build entry: {ship["id"]}')
    report['texture_identity_count']=len(owners)
    icon_text=(stage/'ship/icons/shipicons.lua').read_text(encoding='utf-8')
    for identifier,native in ICON_MAPPING.items():
        if f'{identifier} = {native}' not in icon_text:report['errors'].append('Missing Kushan portrait: '+identifier)
    report['kushan_icon_aliases']=len(ICON_MAPPING)
    report['archive_crc_passed']='TEST: PASSED' in Path('local/VastReachesDemo.test.log').read_text()
    built=Path('local/VastReachesDemo.big')
    installed=Path(r'C:\Program Files (x86)\Steam\steamapps\common\Homeworld\HomeworldRM\Data\VastReachesDemo.big')
    for name,path in (('built',built),('installed',installed)):
        with path.open('rb') as stream:report[name+'_sha256']=hashlib.file_digest(stream,'sha256').hexdigest()
    report['installed_matches']=report['built_sha256']==report['installed_sha256']
    if live:
        log=Path('local/HWRM-test.log').read_text(errors='replace').replace('\0','')
        scene=log.rsplit('VR_GALLERY: init',1)[-1]
        counts={int(i):(ship,int(count)) for i,ship,count in re.findall(r'VR_GALLERY: object=(\d+) type=(\S+) count=(\d+)',scene)}
        report['live_loaded']=sum(counts.get(e['index'])==(e['id'],1) for e in gallery)
        references={int(i):(ship,int(count)) for i,ship,count in re.findall(r'VR_GALLERY: reference=(\d+) type=(\S+) count=(\d+)',scene)}
        report['reference_expected']=sum(bool(e['native']) for e in gallery)
        report['references_loaded']=sum(references.get(e['index'])==(e['native'],1) for e in gallery if e['native'])
        report['scene_ready']=f'VR_GALLERY: ready objects={len(gallery)}' in scene
        report['live_icons_loaded']=f'VR_GALLERY: kushan_icons={len(ICON_MAPPING)}' in scene
        report['views_observed']=[int(i) for i in re.findall(r'VR_GALLERY: view=(\d+)',scene)]
        report['scene_errors']=[s for s in scene.splitlines() if 'stack traceback' in s or 'parameter:' in s]
        if (report['live_loaded']!=len(gallery) or report['references_loaded']!=report['reference_expected']
                or not report['scene_ready'] or not report['live_icons_loaded'] or report['scene_errors']):
            report['errors'].append('Live gallery load is incomplete or contains Lua errors')
    report['passed']=not report['errors'] and report['archive_crc_passed'] and report['installed_matches']
    Path('local/gallery-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='models'},ensure_ascii=False,indent=2))
    if not report['passed']:raise SystemExit('Gallery verification failed')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--live',action='store_true')
    verify(parser.parse_args().live)
