"""Check requested hull gaps, physical sizes, LOD coverage and repaired materials."""

import json
import math
import re
from pathlib import Path

from PIL import Image,ImageStat

from model_size import bounds,native_path
from native_geometry import meshes
from refresh_model_bounds import dae_bounds


def verify():
    stage=Path('local/testmod');errors=[]
    entries=json.loads(Path('local/gallery-manifest.json').read_text(encoding='utf-8'))
    groups=json.loads(Path('local/gallery-groups.json').read_text(encoding='utf-8'))
    spawns=json.loads(Path('local/gallery-spawn-bounds.json').read_text(encoding='utf-8'))
    models={s['id']:s for s in json.loads((stage/'catalogue-manifest.json').read_text(encoding='utf-8'))}
    close=lambda a,b:abs(a-b)<.005
    for entry in entries:
        if entry['native'] and not close(entry['pair_gap'],max(entry['vr_width'],entry['rm_width'])):
            errors.append('Incorrect pair gap: '+entry['id'])
        for ident in filter(None,(entry['id'],entry['native'])):
            text=(stage/'ship'/ident/(ident+'.ship')).read_text(encoding='utf-8-sig')
            for field in ('nlips','nlipsFar'):
                value=re.search(rf'(?m)^NewShipType\.{field}\s*=\s*([\d.]+)',text)
                if not value or float(value[1])!=0:errors.append('Camera scaling enabled: '+ident+'/'+field)
    for group in groups:
        members=[e for e in entries if e['category_group']==group['index']]
        rows={round(e['center'][2],3) for e in members}
        for z in rows:
            row=sorted((e for e in members if round(e['center'][2],3)==z),key=lambda e:e['center'][0])
            for a,b in zip(row,row[1:]):
                actual=b['world_bounds'][0]-a['world_bounds'][3]
                expected=a['trailing_width']+b['leading_width']
                if not close(actual,expected):errors.append(f'Incorrect same-class gap: {a["id"]}/{b["id"]}')
        previous=next((g for g in groups if g['faction']==group['faction'] and g['category']==group['category']-1),None)
        if previous:
            actual=group['bounds'][2]-previous['bounds'][5]
            if not close(actual,max(group['hull_length'],previous['hull_length'])):
                errors.append('Incorrect class gap: '+str(group['index']))
    for i,a in enumerate(spawns):
        for b in spawns[i+1:]:
            overlap=[min(a['bounds'][k+3],b['bounds'][k+3])-max(a['bounds'][k],b['bounds'][k]) for k in range(3)]
            if min(overlap)>.01:errors.append(f'Intersecting hulls: {a["group"]}/{b["group"]}')
    scaled={}
    for ident,model in models.items():
        actual=dae_bounds(Path(model['folder'])/'ship.dae')
        if actual!=model['lod_bounds']:errors.append('Stale LOD bounds: '+ident)
        normalization=model.get('normalization')
        if normalization:
            native=normalization['target_bounds'];zero=actual['0']
            longest=max(zero[a+3]-zero[a] for a in range(3))
            expected=max(native[a+3]-native[a] for a in range(3))
            relative=abs(longest/expected-1)
            scaled[ident]=dict(longest=longest,native_longest=expected,relative_error=relative)
            if relative>.0051:errors.append('Incorrect physical hull size: '+ident)
    damaged=models['vr_destroyer_damaged'];whole=models['rad_destroyer']
    if damaged['lod_bounds']!=whole['lod_bounds']:errors.append('Damaged destroyer geometry scale differs from intact hull')
    materials={}
    for ident in ('vr_stationwing','vr_stationconsole','vr_kus_mothership_door'):
        model=models[ident];items=[]
        for prefix in model['texture_prefixes']:
            folder=Path(model['folder']);report=json.loads((folder/(prefix+'.material.json')).read_text())
            diffuse=Image.open(folder/(prefix+'_DIFF.tga')).convert('RGB')
            deviation=ImageStat.Stat(diffuse).stddev
            items.append(dict(bindings=report['source_bindings'],resolution=diffuse.size,stddev=deviation))
            if diffuse.width<1024 or max(deviation)<5:errors.append('Missing source material detail: '+ident)
            if ident!='vr_kus_mothership_door' and set(report['source_bindings'])!={'BC','N','MSEE'}:
                errors.append('Station array maps incomplete: '+ident)
        materials[ident]=items
    door_path=native_path('vr_reference_kus_door')
    extracted=meshes(door_path)
    original=[m for m in meshes(native_path('kus_mothership')) if m['name']=='moshipdoor_mesh']
    if extracted!=original:errors.append('Isolated HWRM door no longer matches the original mesh')
    comparisons={e['id']:e['native'] for e in entries}
    for ident,native in (('rad_missilecorvette','tai_multiguncorvette'),('rad_frigate','tai_assaultfrigate'),
                         ('rad_destroyer','tai_destroyer'),('vr_destroyer_damaged','tai_destroyer'),
                         ('nku_proximitysensor','kus_proximitysensor'),('vr_kus_mothership_door','vr_reference_kus_door')):
        if comparisons.get(ident)!=native:errors.append('Wrong visual counterpart: '+ident)
    for ident in ('rad_missilecorvette','rad_frigate','rad_destroyer'):
        text=(stage/'ship'/ident/(ident+'.ship')).read_text()
        if not re.search(r'NewShipType.BuildFamily="\w+_Vgr"',text):errors.append('Radaa build family mismatch: '+ident)
    report=dict(passed=not errors,errors=errors,exhibits=len(entries),native_comparisons=sum(bool(e['native']) for e in entries),
                physical_spawns=len(spawns),all_lod_bounds_checked=len(models),sizes=scaled,materials=materials,
                original_native_door_verified=extracted==original,damaged_destroyer_matches_intact=damaged['lod_bounds']==whole['lod_bounds'])
    Path('local/physical-gallery-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('sizes','materials')},ensure_ascii=False,indent=2))
    if errors:raise SystemExit('Physical gallery verification failed')


if __name__=='__main__':verify()
