"""Compare actual mesh geometry and texture atlases, without starting either game."""
import array
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

import UnityPy
from PIL import Image,ImageChops,ImageStat
from UnityPy.helpers.MeshHelper import MeshHandler

PROJECT=Path(__file__).resolve().parent.parent
ROOTS={
    'steam':Path(r'C:\Program Files (x86)\Steam\steamapps\common\Homeworld Vast Reaches Demo\HomeworldVastReachesDemo_Data'),
    'quest':PROJECT/'local/quest-content/HomeworldVastReachesDemo_Data',
}
OUT=PROJECT/'local/quest-comparison.json'


def digest(values):return hashlib.sha256(repr(values).encode('ascii')).hexdigest()


def meshes(env):
    result={}
    for o in env.objects:
        if o.type.name!='Mesh':continue
        name=o.peek_name() or ''
        if name in result:continue
        if not re.search(r'(Kus|Rad|Hgn|Ben|Asteroid|Ship|Shatter|Tower)',name,re.I):continue
        m=o.parse_as_object();h=MeshHandler(m);h.process()
        points=[tuple(round(float(x),6) for x in p[:3]) for p in h.m_Vertices]
        uv=[tuple(round(float(x),6) for x in p[:2]) for p in h.m_UV0] if h.m_UV0 else []
        triangles=[tuple(t) for sub in h.get_triangles() for t in sub]
        canonical=sorted(tuple(sorted(points[i] for i in t)) for t in triangles)
        result[name]={'vertices':len(points),'triangles':len(triangles),'submeshes':len(m.m_SubMeshes),
                      'positions_hash':digest(sorted(points)), 'surface_hash':digest(canonical),
                      'uv_hash':digest(sorted(zip(points,uv))) if uv else None,
                      'bounds':[[min(p[a] for p in points),max(p[a] for p in points)] for a in range(3)] if points else [],
                      'source':o.assets_file.name,'path_id':o.path_id}
    return result


def textures(env):
    result={}
    for o in env.objects:
        if o.type.name!='Texture2D':continue
        name=o.peek_name() or ''
        if not re.match(r'(T_|Kus_|Rad_|Ben_|Hgn_)',name):continue
        d=o.parse_as_dict()
        if name not in result or d['m_Width']*d['m_Height']>result[name]['width']*result[name]['height']:
            result[name]={'width':d['m_Width'],'height':d['m_Height'],'format':d['m_TextureFormat'],'source':o.assets_file.name,'path_id':o.path_id,'object':o}
    return result


def load(data):
    env=UnityPy.Environment();env.path=str(data)
    for p in sorted(data.iterdir()):
        if p.suffix=='.assets' or re.fullmatch(r'level\d+|[0-9a-f]{32}',p.name):env.load_file(str(p))
    return env


def main():
    output={};samples={}
    for platform,root in ROOTS.items():
        print('Reading',platform,flush=True)
        env=load(root)
        result=meshes(env)
        ts=textures(env)
        samples[platform]={}
        failures=[]
        for name,d in ts.items():
            if name.startswith('T_') and re.search(r'(Kus|Rad|Bentusi|Ben|Asteroid)',name,re.I):
                try:samples[platform][name]=d['object'].parse_as_object().image.convert('RGBA').resize((64,64),Image.Resampling.BOX)
                except Exception as exc:failures.append({'name':name,'error':str(exc)[:200]})
        for d in ts.values():d.pop('object')
        output[platform]={'meshes':result,'textures':ts,'texture_decode_failures':failures}
        del env
        print(platform,len(result),'mesh names,',len(ts),'texture names',flush=True)
    same=set(output['steam']['meshes'])&set(output['quest']['meshes'])
    comparison=[]
    for name in sorted(same):
        a,b=output['steam']['meshes'][name],output['quest']['meshes'][name]
        comparison.append({'name':name,'same_vertices':a['vertices']==b['vertices'],'same_triangle_count':a['triangles']==b['triangles'],
                           'same_surface':a['surface_hash']==b['surface_hash'],'same_uv':a['uv_hash']==b['uv_hash'],
                           'steam_vertices':a['vertices'],'quest_vertices':b['vertices'],'steam_triangles':a['triangles'],'quest_triangles':b['triangles']})
    texture_comparison=[]
    for name in sorted(set(output['steam']['textures'])&set(output['quest']['textures'])):
        a,b=output['steam']['textures'][name],output['quest']['textures'][name]
        row={'name':name,'steam_size':[a['width'],a['height']],'quest_size':[b['width'],b['height']],'steam_format':a['format'],'quest_format':b['format']}
        if name in samples['steam'] and name in samples['quest']:
            row['rgba_64px_rms_difference']=ImageStat.Stat(ImageChops.difference(samples['steam'][name],samples['quest'][name])).rms
        texture_comparison.append(row)
    output['comparison']={'meshes':comparison,'textures':texture_comparison,'steam_only_meshes':sorted(set(output['steam']['meshes'])-same),'quest_only_meshes':sorted(set(output['quest']['meshes'])-same)}
    OUT.write_text(json.dumps(output,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'common_meshes':len(same),'equal_surface':sum(r['same_surface'] for r in comparison),'equal_uv':sum(r['same_uv'] for r in comparison),'common_textures':len(texture_comparison),'output':str(OUT)}))


if __name__=='__main__':main()
