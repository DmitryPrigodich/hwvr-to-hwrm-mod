"""Record conservative physical bounds across every exported visible LOD."""

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from model_size import box


def dae_bounds(path):
    ns={'c':'http://www.collada.org/2005/11/COLLADASchema'};lods={}
    for geometry in ET.parse(path).findall('.//c:geometry',ns):
        name=geometry.get('name','')
        match=re.fullmatch(r'MULT\[.*\]_LOD\[(\d+)\]',name)
        if not match:continue
        mesh=geometry.find('c:mesh',ns)
        position_id=mesh.find('c:vertices/c:input[@semantic="POSITION"]',ns).get('source')[1:]
        values=list(map(float,mesh.find(f'c:source[@id="{position_id}"]/c:float_array',ns).text.split()))
        lods.setdefault(match[1],[]).extend(zip(*[iter(values)]*3))
    return {key:box(points) for key,points in lods.items()}


def refresh():
    path=Path('local/catalogue-manifest.json');models=json.loads(path.read_text(encoding='utf-8'))
    for model in models:
        model['lod_bounds']=dae_bounds(Path(model['folder'])/'ship.dae')
        boxes=list(model['lod_bounds'].values())
        model['bounds']=[min(b[a] for b in boxes) for a in range(3)]+[max(b[a+3] for b in boxes) for a in range(3)]
    path.write_text(json.dumps(models,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Recorded all-LOD hull bounds for {len(models)} catalogue models')


if __name__=='__main__':refresh()
