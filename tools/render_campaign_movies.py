"""Flatten extracted VR panoramas/portraits into experimental HWRM WebM movies.

Original scene timing is preserved; this does not emulate Unity's 3D animation.
Run with project Python; NumPy can be borrowed from the bundled desktop runtime.
"""
from __future__ import annotations
import argparse
import functools
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

try:
    import numpy as np
except ModuleNotFoundError:
    sys.path.append(str(Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/python/Lib/site-packages'))
    import numpy as np
from PIL import Image, ImageDraw, ImageFont
import UnityPy

from campaign_cinematic_sources import ROOT, scan_scenes
from prepare_intro_sources import GAME, save_json

WORK = ROOT/'local/cinematic-update/render'
OUTPUT = ROOT/'local/cinematic-update/movies'
FFMPEG = ROOT/'local/cinematic-preparation/ffmpeg.exe'
WIDTH, HEIGHT, FPS = 1280,720,30


def rotation(q):
    x,y,z,w = (q[c] for c in 'xyzw')
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],
                     [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],
                     [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]],dtype=np.float64)


class Renderer:
    def __init__(self, graph, scene, package):
        self.graph,self.scene,self.package = graph,scene,package
        self.rows = graph.rows(scene['scene_source'])
        self.transforms = {r['data']['m_GameObject']['m_PathID']:r for r in self.rows.values() if r['class_name'] in ('Transform','RectTransform')}
        self.env = UnityPy.Environment();self.env.path = str(GAME.resolve());self.files = {}
        self.images = {}
        for image in json.loads((package/'manifest.json').read_text(encoding='utf8'))['images']:
            self.images.setdefault((image['source'],image['path_id']),[]).append(image)
        self.bindings = {graph.address(scene['scene_source'],b['key']):graph.address(scene['scene_source'],b['value']) for b in scene['director']['data']['m_SceneBindings']}
        poser = next(r for r in self.rows.values() if r['class_name']=='Hercules.Designer.PlayerPoser' and r['data']['<CalibrationMode>k__BackingField']==2)
        self.camera = self.world(self.transforms[poser['data']['m_GameObject']['m_PathID']]['path_id'])
        self.focal = HEIGHT/(2*math.tan(math.radians(60)/2))
        self.sky = [];self.sprites=[];self.fades=[]
        for clip in scene['visual_clips']:
            if clip['effectively_muted']:continue
            if clip['class_name']=='Hercules.SkyboxControlAsset':
                material_address = graph.address(clip['asset_source'],clip['data']['Skybox'])
                material = self.get(material_address).parse_as_dict()
                tex = next(value['m_Texture'] for name,value in material['m_SavedProperties']['m_TexEnvs'] if name=='_Tex')
                self.sky.append((clip['start'],graph.address(material_address[0],tex)))
            elif clip['class_name']=='Hercules.BillboardAsset':
                address = graph.address(clip['asset_source'],clip['data']['Sprite'])
                bound = self.bindings.get((clip['track_source'],clip['track']))
                if address and bound:
                    component = self.get(bound).parse_as_dict()
                    self.sprites.append(self.sprite(clip,address,component['m_GameObject']['m_PathID']))
            elif clip['class_name']=='Hercules.CameraFadeAsset':
                self.fades.append((clip['start'],clip['duration'],clip['data']['color']['a']))
        self.sky.sort();self.fades.sort()
        self.omitted_3d = []
        for track in scene['tracks']:
            if track['effectively_muted'] or track['class_name']!='UnityEngine.Timeline.ActivationTrack':continue
            bound = self.bindings.get((track['source'],track['path_id']))
            if not bound:continue
            gameobject = self.graph.rows(bound[0]).get(bound[1])
            if not gameobject:continue
            name = gameobject.get('name','')
            if name.startswith('ANIM_'):
                self.omitted_3d.append(name)
            if name=='T_M11_Pt2_Schematics':
                obj = self.get(bound).parse_as_dict()
                for ref in obj['m_Component']:
                    component = self.get(graph.address(bound[0],ref['component']))
                    if component.type.name=='SpriteRenderer':
                        data=component.parse_as_dict();address=graph.address(bound[0],data['m_Sprite'])
                        asset=self.get(address).parse_as_object()
                        folder=WORK/(scene['mission']+'_extra');folder.mkdir(parents=True,exist_ok=True)
                        path=folder/'schematics.png';asset.image.save(path)
                        self.images[address]=[{'path':str(path),'size':list(asset.image.size)}]
                        for clip in track['data'].get('m_Clips',[]):
                            self.sprites.append(self.sprite({'start':clip['m_Start'],'duration':clip['m_Duration']},address,bound[1]))

    def get(self,address):
        source,ident=address
        if source not in self.files:self.files[source]=self.env.load_file(str((GAME/source).resolve()))
        return self.files[source].objects[ident]

    @functools.lru_cache(maxsize=None)
    def world(self,ident):
        d=self.rows[ident]['data'];m=np.eye(4)
        m[:3,:3]=rotation(d['m_LocalRotation'])@np.diag([d['m_LocalScale'][c] for c in 'xyz'])
        m[:3,3]=[d['m_LocalPosition'][c] for c in 'xyz']
        parent=d['m_Father']['m_PathID']
        return self.world(parent)@m if parent else m

    def sprite(self,clip,address,go):
        asset=self.get(address).parse_as_object()
        matrix=self.world(self.transforms[go]['path_id'])
        center=np.linalg.inv(self.camera)@matrix[:,3]
        width,height=self.images[address][0]['size']
        ppu=asset.m_PixelsToUnits
        scale=np.linalg.norm(matrix[:3,:3],axis=0)
        return {'start':clip['start'],'duration':clip['duration'],'address':address,'center':center[:3].tolist(),'size_world':[width/ppu*scale[0],height/ppu*scale[1]]}

    @functools.lru_cache(maxsize=8)
    def panorama(self,address):
        xx,yy=np.meshgrid((np.arange(WIDTH)+.5-WIDTH/2)/self.focal,(HEIGHT/2-np.arange(HEIGHT)-.5)/self.focal)
        rays=np.stack([xx,yy,np.ones_like(xx)],axis=-1)@self.camera[:3,:3].T
        x,y,z=[rays[:,:,i] for i in range(3)];ax,ay,az=np.abs(x),np.abs(y),np.abs(z)
        major=np.argmax(np.abs(rays),axis=-1);result=np.zeros((HEIGHT,WIDTH,3),dtype=np.uint8)
        configs={'positive_x':((major==0)&(x>=0),-z/np.maximum(ax,1e-9),-y/np.maximum(ax,1e-9)),
                 'negative_x':((major==0)&(x<0),z/np.maximum(ax,1e-9),-y/np.maximum(ax,1e-9)),
                 'positive_y':((major==1)&(y>=0),x/np.maximum(ay,1e-9),z/np.maximum(ay,1e-9)),
                 'negative_y':((major==1)&(y<0),x/np.maximum(ay,1e-9),-z/np.maximum(ay,1e-9)),
                 'positive_z':((major==2)&(z>=0),x/np.maximum(az,1e-9),-y/np.maximum(az,1e-9)),
                 'negative_z':((major==2)&(z<0),-x/np.maximum(az,1e-9),-y/np.maximum(az,1e-9))}
        for row in self.images[address]:
            mask,u,v=configs[row['face']]
            if not np.any(mask):continue
            with Image.open(self.package/row['path']) as image: pixels=np.array(image.convert('RGB'))
            sx=np.clip((u[mask]+1)*.5*(pixels.shape[1]-1),0,pixels.shape[1]-1)
            sy=np.clip((v[mask]+1)*.5*(pixels.shape[0]-1),0,pixels.shape[0]-1)
            x0=sx.astype(int);y0=sy.astype(int);x1=np.minimum(x0+1,pixels.shape[1]-1);y1=np.minimum(y0+1,pixels.shape[0]-1)
            fx=(sx-x0)[:,None];fy=(sy-y0)[:,None]
            sample=(pixels[y0,x0]*(1-fx)*(1-fy)+pixels[y0,x1]*fx*(1-fy)+pixels[y1,x0]*(1-fx)*fy+pixels[y1,x1]*fx*fy)
            result[mask]=np.rint(sample).astype(np.uint8)
        return Image.fromarray(result).convert('RGBA')

    def alpha(self,t):
        alpha=0.
        for start,duration,target in self.fades:
            if t<start:break
            if t<start+duration:return alpha+(target-alpha)*(t-start)/duration
            alpha=target
        return max(alpha,min(1.,max(0.,(t-(self.scene['duration_seconds']-.3))/.3)))

    def frame(self,t,language,cues):
        address=next((a for start,a in reversed(self.sky) if start<=t),self.sky[0][1])
        image=self.panorama(address).copy()
        for sprite in self.sprites:
            if not sprite['start']<=t<sprite['start']+sprite['duration']:continue
            x,y,z=sprite['center']
            if z<=0:continue
            row=self.images[sprite['address']][0]
            portrait=Image.open(self.package/row['path']).convert('RGBA')
            w=max(1,round(sprite['size_world'][0]*self.focal/z));h=max(1,round(sprite['size_world'][1]*self.focal/z))
            portrait=portrait.resize((min(w,4096),min(h,4096)),Image.Resampling.LANCZOS)
            pos=(round(WIDTH/2+x*self.focal/z-w/2),round(HEIGHT/2-y*self.focal/z-h/2))
            image.alpha_composite(portrait,pos)
        opacity=self.alpha(t)
        if opacity>0:image=Image.blend(image,Image.new('RGBA',image.size,'black'),opacity)
        text='\n'.join(c[language] for c in cues if c['start']<=t<c['start']+c['duration'])
        if text:
            font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',23)
            measure=ImageDraw.Draw(image);lines=[]
            for paragraph in text.split('\n'):
                line=''
                for word in paragraph.split():
                    candidate=(line+' '+word).strip()
                    if measure.textlength(candidate,font=font)>WIDTH-100 and line:lines.append(line);line=word
                    else:line=candidate
                if line:lines.append(line)
            panel=Image.new('RGBA',image.size);draw=ImageDraw.Draw(panel)
            top=HEIGHT-22-len(lines)*29
            draw.rectangle((24,top-12,WIDTH-24,HEIGHT-10),fill=(0,0,0,195))
            for i,line in enumerate(lines):
                draw.text(((WIDTH-draw.textlength(line,font=font))/2,top+i*29),line,font=font,fill='white')
            image=Image.alpha_composite(image,panel)
        return image.convert('RGB')


def render_scene(graph,scene,package,encode=True):
    name=package.name;directory=WORK/name;directory.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((package/'manifest.json').read_text(encoding='utf8'))
    cues=[c for c in manifest['dialogue_cues'] if not c.get('effectively_muted')]
    renderer=Renderer(graph,scene,package)
    end=math.ceil(scene['duration_seconds']*FPS)
    boundaries={0,end}
    for clip in scene['visual_clips']+cues:
        if clip.get('effectively_muted'):continue
        for time in (clip['start'],clip['start']+clip['duration']):boundaries.add(max(0,min(end,round(time*FPS))))
    for start,duration,target in renderer.fades+[(scene['duration_seconds']-.3,.3,1)]:
        boundaries.update(range(max(0,round(start*FPS)),min(end,math.ceil((start+duration)*FPS))+1))
    boundaries=sorted(boundaries)
    OUTPUT.mkdir(parents=True,exist_ok=True)
    videos=[]
    for lang in ('ru','en'):
        pages=[]
        for index,(a,b) in enumerate(zip(boundaries,boundaries[1:])):
            t=(a+b)/(2*FPS);path=directory/f'{lang}_{index:04d}.png'
            renderer.frame(t,lang,cues).save(path)
            pages.append(f"file '{path.as_posix()}'\nduration {(b-a)/FPS:.9f}")
        pages.append(f"file '{path.as_posix()}'")
        listing=directory/f'{lang}.concat';listing.write_text('\n'.join(pages)+'\n',encoding='utf8')
        movie=OUTPUT/f'{name}.{lang}.webm'
        voice=package/('audio/prologue_voice_timeline.wav' if name=='prologue' else manifest['voice_reference']['reference'])
        stems=[]
        for row in manifest['stems']:
            stems.extend([{**item,'event':row['event']} for item in row['media']] if 'media' in row else [row])
        command=[str(FFMPEG),'-y','-hide_banner','-loglevel','warning','-f','concat','-safe','0','-i',str(listing),'-i',str(voice)]
        for stem in stems:command+=['-i',str(package/stem['wav'])]
        filters=['[1:a]volume=1[voice]'];labels=['[voice]']
        for i,stem in enumerate(stems,2):
            gain=.28 if 'music' in stem.get('event',str(stem.get('short_name',''))).lower() else .35
            if stem['channels']==4:filters.append(f'[{i}:a]pan=stereo|c0=0.75*c0+0.25*c2|c1=0.75*c1+0.25*c3,volume={gain}[s{i}]')
            else:filters.append(f'[{i}:a]aformat=channel_layouts=stereo,volume={gain}[s{i}]')
            labels.append(f'[s{i}]')
        filters.append(''.join(labels)+f'amix=inputs={len(labels)}:duration=first:normalize=0,alimiter=limit=0.95:level=false,afade=t=out:st={end/FPS-.5}:d=0.5[a]')
        filterfile=directory/f'{lang}.filters';filterfile.write_text(';'.join(filters),encoding='ascii')
        command+=['-filter_complex_script',str(filterfile),'-map','0:v','-map','[a]','-r',str(FPS),'-fps_mode','cfr','-c:v','libvpx','-deadline','good','-cpu-used','5','-threads','4','-b:v','1800k','-crf','15','-g','120','-pix_fmt','yuv420p','-c:a','libvorbis','-q:a','5','-ar','44100','-t',f'{end/FPS:.9f}',str(movie)]
        (directory/f'{lang}.command.json').write_text(json.dumps(command,indent=2),encoding='utf8')
        if encode:
            with (directory/f'{lang}.encode.log').open('w',encoding='utf8') as log:
                subprocess.run(command,stdout=log,stderr=log,check=True)
        videos.append({'language':lang,'path':str(movie),'sha256':hashlib.sha256(movie.read_bytes()).hexdigest() if movie.exists() else None,'bytes':movie.stat().st_size if movie.exists() else None})
    report={'package':name,'mission':scene['mission'],'field':scene['field'],'duration_seconds':end/FPS,'source_duration_seconds':scene['duration_seconds'],'resolution':[WIDTH,HEIGHT],'fps':FPS,'videos':videos,'camera':'source PlayerPoser_Animatic position/rotation; fixed perspective; vertical FOV60','audio_mix':'voice1; music0.28; ambience0.35; quad downmix75%front/25%rear; peak limiter0.95; selected adaptation levels, not original Wwise mix','omitted_3d_objects':renderer.omitted_3d,'status':'experimental_flat_adaptation; no_engine_test'}
    save_json(directory/'render.json',report)
    print(json.dumps(report,ensure_ascii=False),flush=True)
    renderer.panorama.cache_clear();renderer.world.cache_clear()
    return report


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--scenes',nargs='*');parser.add_argument('--frames-only',action='store_true');args=parser.parse_args()
    graph,scenes=scan_scenes();index=json.loads((ROOT/'campaign-export/cinematics/index.json').read_text(encoding='utf8'))['scenes']
    reports=[]
    for scene,entry in zip(scenes,index,strict=True):
        assert scene['mission']==entry['mission'] and scene['field']==entry['field']
        if args.scenes and entry['directory'] not in args.scenes:continue
        print('Rendering '+entry['directory'],flush=True)
        reports.append(render_scene(graph,scene,ROOT/'campaign-export/cinematics'/entry['directory'],not args.frames_only))
    save_json(WORK/'latest-render.json',reports)


if __name__=='__main__':main()
