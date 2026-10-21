"""Stage imported hulls as buildable prototypes and scenery as inspection objects."""

import json
import re
import shutil
from pathlib import Path

from borrow_native_rig import borrow
from catalogue import native_folder
from source_weapon_mounts import apply as apply_source_mounts
from physical_display import configure


def family_for(spec, template):
    family = re.search(r'NewShipType.BuildFamily\s*=\s*"([^"]+)"',template)[1]
    if spec.get('race') == 'novokushan':
        family=family.replace('_Hgn','_Kus')
        family={'Shipyard_Kus':'SuperCap_Kus','Utility_Kus':'Resource_Kus','Platform_Kus':'Resource_Kus'}.get(family,family)
    elif spec.get('race')=='radaa':
        family=family.replace('_Tai','_Vgr')
    return family


def prepare(destination, translations):
    manifest=Path('local/catalogue-manifest.json')
    if not manifest.exists():return []
    models=json.loads(manifest.read_text(encoding='utf-8'))
    buildable=[]
    for i,spec in enumerate(models):
        archetype=spec.get('archetype') or 'hgn_probe'
        source=native_folder(archetype)
        template=(source/(archetype+'.ship')).read_text(encoding='utf-8-sig')
        native_template=template
        folder=destination/'ship'/spec['id'];folder.mkdir(parents=True,exist_ok=True)
        hod=folder/(spec['id']+'.hod');shutil.copyfile(Path(spec['folder'])/'ship.hod',hod)
        if spec.get('archetype'):
            spec['native_rig']=borrow(hod,source/(archetype+'.hod'))
        # New hull engine meshes use different transforms from the borrowed rig.
        template='\n'.join(line for line in template.splitlines() if not re.match(
            r'\s*(setEngineTrail|setEngineBurn|setEngineGlow)\(',line))
        ucs=9902000+2*i
        template=re.sub(r'NewShipType.displayedName=.*',f'NewShipType.displayedName="${ucs}"',template)
        template=re.sub(r'NewShipType.sobDescription=.*',f'NewShipType.sobDescription="${ucs+1}"',template)
        batch=re.search(r'NewShipType.buildBatch=getShipNum\([^\n]+,\s*(\d+)\)',template)
        if batch and int(batch[1])>1:
            count=int(batch[1])
            for field in ('buildCost','buildTime'):
                match=re.search(rf'NewShipType.{field}=(\d+)',template)
                if match:template=re.sub(rf'NewShipType.{field}=.*',f'NewShipType.{field}={max(1,round(int(match[1])/count))}',template)
        template+='\nNewShipType.buildBatch=1\nNewShipType.SquadronSize=1\n'
        if spec.get('buildable'):
            family=family_for(spec,template)
            template=re.sub(r'NewShipType.BuildFamily=.*',f'NewShipType.BuildFamily="{family}"',template)
            if '"CanBuildShips"' in template:
                families=('Fighter_Kus, Corvette_Kus, Frigate_Kus, SuperCap_Kus, Resource_Kus, NonCombat_Kus'
                          if spec['race']=='novokushan' else
                          'Fighter_Vgr, Corvette_Vgr, Frigate_Vgr, SuperCap_Vgr, Utility_Vgr, Platform_Vgr, Shipyard_Vgr, Probe_Vgr')
                template=re.sub(r'^addAbility\(NewShipType,"CanBuildShips"[^\n]*',
                    f'addAbility(NewShipType,"CanBuildShips",1,"{families}","Fighter, Corvette, Frigate, Capital, Resource, NonCombat, Utility, Platform");',template,flags=re.MULTILINE)
            buildable.append({**spec,'ucs':ucs,'ru':spec['ru']+' VR','en':spec['id'],'family':family})
        else:
            template=re.sub(r'^StartShipWeaponConfig[^\n]*','',template,flags=re.MULTILINE)
            template+='\nNewShipType.maxspeed=0\n'
        events=source/(archetype+'.events')
        event_text=events.read_text(encoding='utf-8-sig') if events.exists() else ''
        template,event_text,mount_report=apply_source_mounts(hod,spec,template,event_text,native_template)
        if mount_report:spec['source_weapon_mounts']=mount_report
        (folder/(spec['id']+'.ship')).write_text(configure(template)+'\n',encoding='utf-8')
        if event_text:(folder/(spec['id']+'.events')).write_text(event_text,encoding='utf-8')
        for language in ('Russian','English'):
            translations[language][ucs]=spec['ru']+' VR' if language=='Russian' else spec['id']
            translations[language][ucs+1]=(
                f'Модель из демки Vast Reaches. Временная основа HWRM: {archetype}. Способности Unity ещё не восстановлены.'
                if spec.get('buildable') else 'Объект из демки Vast Reaches для осмотра.')
        spec['ucs']=ucs
    (destination/'catalogue-manifest.json').write_text(json.dumps(models,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Staged {len(models)} catalogue objects, {len(buildable)} additional buildable ships')
    return buildable
