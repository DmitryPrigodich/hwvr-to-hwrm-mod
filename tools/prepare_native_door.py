"""Isolate the actual animated door mesh from the installed Kushan mothership."""

import hashlib
import json
from pathlib import Path

from PIL import Image

from borrow_native_rig import chunks,form
from build_hod import build
from export_ship import write_dae
from model_size import box,native_path
from native_geometry import meshes,mesh_chunks
from physical_display import configure
from source_weapon_mounts import read_hierarchy,write_hierarchy


IDENTIFIER='vr_reference_kus_door'


def prepare():
    source=native_path('kus_mothership');binary=source.read_bytes()
    folder=Path('local/gallery-native/ship')/IDENTIFIER;folder.mkdir(parents=True,exist_ok=True)
    provenance=folder/'source.json';digest=hashlib.sha256(binary).hexdigest()
    output=folder/(IDENTIFIER+'.hod')
    if output.exists() and provenance.exists() and json.loads(provenance.read_text())['sha256']==digest:return
    geometry=[m for m in meshes(source) if m['name']=='moshipdoor_mesh']
    points=[p for m in geometry for part in m['parts'] for p in part['positions']]
    hull=box(points)
    corners=[(hull[3] if i&1 else hull[0],hull[4] if i&2 else hull[1],hull[5] if i&4 else hull[2]) for i in range(8)]
    faces=[(0,2,3),(0,3,1),(4,5,7),(4,7,6),(0,1,5),(0,5,4),(2,6,7),(2,7,3),(0,4,6),(0,6,2),(1,3,7),(1,7,5)]
    obj=''.join('v '+' '.join(map(str,p))+'\n' for p in corners)
    obj+='vt 0 0\n'*8+'vn 0 0 1\n'*8
    obj+=''.join('f '+' '.join(f'{i+1}/{i+1}/{i+1}' for i in f)+'\n' for f in faces)
    Image.new('RGB',(16,16),(128,128,128)).save(folder/'bounds_DIFF.tga')
    write_dae([(0,obj)],'bounds_DIFF.tga',folder/'bounds.dae',1,{})
    build(Path(r'C:\Program Files (x86)\Steam\steamapps\common\Homeworld 347380\GBXTools\HODOR\HODOR.exe'),
          folder/'bounds.dae',folder/'bounds.hod',minimum_size=1024)
    collision=dict(chunks(dict(chunks((folder/'bounds.hod').read_bytes()))[b'DTRM'],12))[b'KDOP']
    # Pooled vertices are consumed in MULT order. The door is the first MULT.
    # Keeping all texture/material records preserves their existing pool indexes.
    mults=list(mesh_chunks(binary))
    if mults[0][0][0]!='moshipdoor_mesh':raise ValueError('Mothership pool layout has changed')
    result=[]
    for kind,chunk in chunks(binary):
        if kind==b'HVMD':
            kept=[c for k,c in chunks(chunk,12) if not(k==b'NRML' and c[8:12]==b'MULT') or c==mults[0][1]]
            chunk=form(b'HVMD',b''.join(kept))
        elif kind==b'DTRM':
            hierarchy=dict(chunks(chunk,12))[b'HIER']
            nodes=[n for n in read_hierarchy(hierarchy) if n['name'] in ('Root','moshipdoor')]
            for node in nodes:node['values']=[0]*9
            chunk=form(b'DTRM',write_hierarchy(nodes)+collision)
        result.append(chunk)
    output.write_bytes(b''.join(result))
    template=Path('local/hw2ships/ship/hgn_probe/hgn_probe.ship').read_text(encoding='utf-8-sig')
    template+='\nNewShipType.maxspeed=0\n'
    (folder/(IDENTIFIER+'.ship')).write_text(configure(template),encoding='utf-8')
    report=dict(source=str(source),sha256=digest,mesh='moshipdoor_mesh',bounds=hull,
                lods=[m['lod'] for m in geometry],method='Original HWRM MULT, POOL, textures and materials; isolated static joint')
    provenance.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('Prepared original HWRM mothership door:',hull)


if __name__=='__main__':prepare()
