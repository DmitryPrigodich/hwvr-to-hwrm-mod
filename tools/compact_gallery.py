"""Pack inspection pairs by faction and class, using each model's real bounds."""

import json
import math
from pathlib import Path

from borrow_native_rig import chunks
from fleet import FLEET
from gallery_layout import all_categories
from model_size import bounds, native_path
from prepare_ship_icons import ICON_MAPPING


KEYS=['ONEKEY','TWOKEY','THREEKEY','FOURKEY','FIVEKEY','SIXKEY','SEVENKEY']


def readable(model):
    name=model.get('mesh','')
    if not name:return model['ru']
    for token,title in (('Mothership_Door','Створка ангара материнского корабля'),('Shield_Sphere','Сфера щита'),
        ('HeavyMissle','Тяжёлая ракета'),('ShatterStation_Attack','Shatter Station: дополнительная модель'),
        ('RadioactiveRock','Радиоактивный астероид'),('Container','Ресурсный контейнер'),
        ('FragmentPanel','Фрагмент панели'),('JunkPanel','Обломок панели'),('JunkSensors','Обломки датчиков')):
        if token in name:return title
    for token,title in (('Asteroid','Ресурсный астероид'),('RubbleMedium','Средний обломок'),
                        ('RubbleSmall','Малый обломок'),('RubbleLarge','Крупный обломок')):
        if token in name:return title+' '+name.rsplit('_',1)[-1]
    if 'RubbleMix' in name:return 'Смешанные обломки'+(' (вариант 2)' if '__' in name else '')
    return model['ru']


def union(boxes):
    boxes=list(boxes)
    return [min(b[a] for b in boxes) for a in range(3)]+[max(b[a+3] for b in boxes) for a in range(3)]


def shifted(box,offset):
    return [v+offset[a%3] for a,v in enumerate(box)]


def camera(name,box):
    center=[(box[a]+box[a+3])/2 for a in range(3)]
    w,h,d=[box[a+3]-box[a] for a in range(3)]
    # 45-degree vertical FOV, with headroom for free camera rotation.
    distance=max(w/(2*.414*1.6),(h*.82+d*.58)/(2*.414),20)*1.2+d*.45
    position=[center[0],center[1]+distance*.58,center[2]+distance*.82]
    fmt=lambda p:', '.join(f'{v:.3f}' for v in p)
    return f'    addCamera("{name}", {{{fmt(center)}}}, {{{fmt(position)}}})'


def prepare():
    manifest=Path('local/catalogue-manifest.json')
    if not manifest.exists():return
    models={m['id']:m for m in json.loads(manifest.read_text(encoding='utf-8'))}
    for ship in FLEET:
        path=Path('exports')/ship['mesh'].lower()/'ship.hod'
        models[ship['id']]={**ship,'bounds':bounds(path)}
    for model in models.values():model['title']=readable(model).removesuffix(' VR')
    factions=[];groups=[];entries=[]
    for faction_index,(faction_name,categories) in enumerate(all_categories(models),1):
        faction=dict(index=faction_index,name=faction_name,groups=[])
        z=0;widest=0;faction_boxes=[];previous_length=0
        for category_index,(category_name,pairs) in enumerate(categories,1):
            group=dict(index=len(groups)+1,faction=faction_index,category=category_index,
                       name=category_name,entries=[],first=len(entries)+1)
            rows=[];row=[]
            columns=4 if faction_name=='MISC' else len(pairs)
            for identifier,native in pairs:
                model=models[identifier];vr_box=model['bounds'];vr_dims=[vr_box[a+3]-vr_box[a] for a in range(3)]
                rm_box=bounds(native_path(native)) if native else None
                rm_dims=[rm_box[a+3]-rm_box[a] for a in range(3)] if rm_box else [0,0,0]
                gap=max(vr_dims[0],rm_dims[0]) if native else 0
                width=vr_dims[0]+rm_dims[0]+gap
                entry=dict(index=len(entries)+1,id=identifier,ru=model['title'],native=native,
                           group=f'Gallery_{len(entries)+1}',ucs=9904001+len(entries),
                           faction=faction_index,category=category_index,category_group=group['index'],
                           vr_bounds=vr_box,rm_bounds=rm_box,dimensions=[width,max(vr_dims[1],rm_dims[1]),max(vr_dims[2],rm_dims[2])],
                           pair_gap=gap,vr_width=vr_dims[0],rm_width=rm_dims[0],
                           hull_length=max(*vr_dims,*rm_dims),
                           leading_width=vr_dims[0],trailing_width=rm_dims[0] if native else vr_dims[0])
                entries.append(entry);row.append(entry);group['entries'].append(entry['index'])
                if len(row)==columns:rows.append(row);row=[]
            if row:rows.append(row)
            group_length=max(e['hull_length'] for row in rows for e in row)
            group['preceding_gap']=max(previous_length,group_length) if previous_length else 0
            z+=group['preceding_gap'];previous_length=group_length
            group['hull_length']=group_length
            cursor_z=0;row_layouts=[];previous_depth=0;previous_row_width=0
            for row in rows:
                depth=max(e['dimensions'][2] for e in row)
                gaps=[a['trailing_width']+b['leading_width'] for a,b in zip(row,row[1:])]
                hull_width=max(max(e['vr_width'],e['rm_width']) for e in row)
                if previous_depth:cursor_z+=previous_row_width+hull_width
                width=sum(e['dimensions'][0] for e in row)+sum(gaps)
                row_layouts.append((row,width,depth,cursor_z,gaps))
                cursor_z+=depth;previous_depth=depth;previous_row_width=hull_width
            group_width=max(r[1] for r in row_layouts);group_depth=cursor_z
            for row,width,depth,row_z,gaps in row_layouts:
                cursor_x=-width/2
                for i,entry in enumerate(row):
                    entry['center']=[cursor_x+entry['dimensions'][0]/2,0,z+row_z+depth/2]
                    entry['next_hull_gap']=gaps[i] if i<len(gaps) else None
                    cursor_x+=entry['dimensions'][0]+(gaps[i] if i<len(gaps) else 0)
            height=max(e['dimensions'][1] for row in rows for e in row)
            group['bounds']=[-group_width/2,-height/2,z,group_width/2,height/2,z+group_depth]
            group['last']=len(entries);group['center']=[0,0,z+group_depth/2]
            group['faction_name']=faction_name
            faction_boxes.append(group['bounds']);widest=max(widest,group_width)
            z+=group_depth
            groups.append(group);faction['groups'].append(group['index'])
        faction['bounds']=union(faction_boxes);factions.append(faction)
    left_width=max(f['bounds'][3]-f['bounds'][0] for f in (factions[0],factions[2]))
    right_width=max(f['bounds'][3]-f['bounds'][0] for f in (factions[1],factions[3]))
    faction_gap=max(g['hull_length'] for g in groups)
    left_x=-(right_width+faction_gap)/2;right_x=(left_width+faction_gap)/2
    bottom_z=max(factions[0]['bounds'][5],factions[1]['bounds'][5])+faction_gap
    for faction,offset in zip(factions,([left_x,0,0],[right_x,0,0],[left_x,0,bottom_z],[right_x,0,bottom_z])):
        faction['bounds']=shifted(faction['bounds'],offset)
        for group_index in faction['groups']:
            group=groups[group_index-1];group['bounds']=shifted(group['bounds'],offset)
            group['center']=[a+b for a,b in zip(group['center'],offset)]
            for index in group['entries']:
                entry=entries[index-1];entry['center']=[a+b for a,b in zip(entry['center'],offset)]
    level=['function DetermChunk()'];labels={};spawn_boxes=[]
    for entry in entries:
        x,y,z=entry['center'];w,h,d=entry['dimensions']
        vr_center=x-w/2+entry['vr_width']/2
        boxes=[]
        sides=[('',entry['id'],entry['vr_bounds'],vr_center)]
        if entry['native']:sides.append(('_RM',entry['native'],entry['rm_bounds'],x+w/2-entry['rm_width']/2))
        for suffix,identifier,box,sx in sides:
            center=[(box[a]+box[a+3])/2 for a in range(3)]
            position=[sx-center[0],-center[1],z-center[2]]
            sob=entry['group']+suffix
            level += [f'    addSquadron("{sob}","{identifier}",{{{position[0]:.3f},{position[1]:.3f},{position[2]:.3f}}},0,{{0,0,0}},1,0)',
                      f'    createSOBGroup("{sob}")',f'    addToSOBGroup("{sob}","{sob}")']
            world=shifted(box,position);boxes.append(world);spawn_boxes.append(dict(group=sob,bounds=world))
        entry['world_bounds']=union(boxes)
        level.append(camera('Gallery_Camera'+str(entry['index']),entry['world_bounds']))
        group=groups[entry['category_group']-1]
        number=group['entries'].index(entry['index'])+1
        label=f'{group["faction_name"]} / {group["name"]}: {number}/{len(group["entries"])} — {entry["ru"]}.'
        label+=' СЛЕВА HWVR, СПРАВА HWRM.' if entry['native'] else ' Модель HWVR.'
        labels[entry['ucs']]=label+' N/P: пары; PgUp/PgDn: группы; 1–7: класс; F1–F4: фракция.'
    for group in groups:
        level.append(camera('Gallery_Group'+str(group['index']),group['bounds']))
        titles='; '.join(entries[i-1]['ru'] for i in group['entries'])
        labels[9906000+group['index']]=f'{group["faction_name"]} / {group["name"]}: {titles}. N/P: осмотр; PgUp/PgDn: группы.'
    for faction in factions:
        level.append(camera('Gallery_Faction'+str(faction['index']),faction['bounds']))
        class_list='; '.join(f'{i+1}: {groups[g-1]["name"]}' for i,g in enumerate(faction['groups']))
        labels[9907000+faction['index']]=f'{faction["name"]}. {class_list}. F1–F4: фракции; 8: общий вид фракции.'
    world=union(f['bounds'] for f in factions)
    level.append(camera('Gallery_Overview',world))
    center=[(world[a]+world[a+3])/2 for a in range(3)];extent=[max(2000,(world[a+3]-world[a])*.8) for a in range(3)]
    level += [f'    setWorldBoundsInner({{{center[0]:.3f},0,{center[2]:.3f}}},{{{extent[0]:.3f},{max(extent):.3f},{extent[2]:.3f}}})',
              'end','function NonDetermChunk()','    loadBackground("m01")',
              f'    setSensorsManagerCameraDistances(10,{max(extent)*4:.3f})','end',
              'levelDesc="Vast Reaches compact faction comparisons"','maxPlayers=2','player={}',
              'player[0]={id=0,name="",resources=999999,raceName="Novokushan",startPos=0}',
              'player[1]={id=1,name="",resources=0,raceName="Radaa",startPos=0}']
    labels[9904000]='F1: Новокушане; F2: Радаа; F3: NPC; F4: MISC. 1–7: класс; N/P: пары; PgUp/PgDn: группы; 8: фракция; 0: карта.'
    folder=Path('mod/leveldata/campaign/VastReachesGallery/Inspect');folder.mkdir(parents=True,exist_ok=True)
    (folder/'Inspect.level').write_text('\n'.join(level)+'\n',encoding='utf-8')
    write_script(folder,entries,groups,factions)
    (folder/'teamcolour.lua').write_text(Path('mod/leveldata/campaign/VastReachesCompare/Compare/teamcolour.lua').read_text(),encoding='utf-8')
    for name,value in (('gallery-labels',labels),('gallery-manifest',entries),('gallery-groups',groups),('gallery-factions',factions),('gallery-spawn-bounds',spawn_boxes)):
        Path('local/'+name+'.json').write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
    write_docs(entries,groups,factions)
    refs=sum(bool(e['native']) for e in entries)
    print(f'Compact gallery: {len(entries)} exhibits, {refs} comparisons, {len(groups)} categories; '
          f'footprint {world[3]-world[0]:.0f} x {world[5]-world[2]:.0f}')


def write_script(folder,entries,groups,factions):
    lua=['dofilepath("data:scripts/SCAR/SCAR_Util.lua")',f'Gallery_Total={len(entries)}',f'Gallery_GroupTotal={len(groups)}',
         'Gallery_Current=1','Gallery_CurrentFaction=1','Gallery_CurrentGroup=1','Gallery_Mode="group"',
         'Gallery_EntryGroups={'+','.join(str(e['category_group']) for e in entries)+'}',
         'Gallery_GroupFactions={'+','.join(str(g['faction']) for g in groups)+'}',
         'Gallery_First={'+','.join(str(g['first']) for g in groups)+'}',
         'Gallery_Last={'+','.join(str(g['last']) for g in groups)+'}',
         'Gallery_FactionGroups={'+','.join('{'+','.join(map(str,f['groups']))+'}' for f in factions)+'}',
         'function OnInit()','    print("VR_GALLERY: init")','    Rule_AddInterval("Gallery_Ready",1)','end',
         'function Gallery_Ready()']
    lua += ['    dofilepath("data:ship/icons/shipicons.lua")','    local iconCount=0']
    for identifier in ICON_MAPPING:
        lua += [f'    if {identifier}~=nil and {identifier}.LargeIcon~=nil then iconCount=iconCount+1 end']
    lua += ['    print("VR_GALLERY: kushan_icons="..iconCount)']
    for entry in entries:
        for suffix in ('','_RM') if entry['native'] else ('',):
            group=entry['group']+suffix
            lua += [f'    SobGroup_AbilityActivate("{group}",AB_Attack,0)',f'    SobGroup_AbilityActivate("{group}",AB_Move,0)',
                    f'    SobGroup_SetMaxSpeed("{group}",0)']
        lua += [f'    print("VR_GALLERY: object={entry["index"]} type={entry["id"]} count="..SobGroup_Count("{entry["group"]}"))']
        if entry['native']:
            lua += [f'    print("VR_GALLERY: reference={entry["index"]} type={entry["native"]} count="..SobGroup_Count("{entry["group"]}_RM"))']
    for i,key in enumerate(KEYS,1):lua += [f'    UI_BindKeyEvent({key},"Gallery_Class{i}")']
    for i in range(1,5):lua += [f'    UI_BindKeyEvent(F{i}KEY,"Gallery_Faction{i}")']
    for key,func in (('NKEY','Gallery_Next'),('PKEY','Gallery_Previous'),('PAGEDOWNKEY','Gallery_NextGroup'),('PAGEUPKEY','Gallery_PreviousGroup'),
                     ('EIGHTKEY','Gallery_FactionOverview'),('NINEKEY','Gallery_FocusFirst'),('ZEROKEY','Gallery_Overview')):
        lua += [f'    UI_BindKeyEvent({key},"{func}")']
    lua += [f'    print("VR_GALLERY: ready objects={len(entries)} references={sum(bool(e["native"]) for e in entries)} groups={len(groups)}")',
            '    Gallery_Category(1)','    Rule_Remove("Gallery_Ready")','end',
            'function Gallery_Show(index)','    Gallery_Current=index','    Gallery_CurrentGroup=Gallery_EntryGroups[index]',
            '    Gallery_CurrentFaction=Gallery_GroupFactions[Gallery_CurrentGroup]','    Gallery_Mode="pair"',
            '    Camera_Interpolate("here","Gallery_Camera"..index,0)','    Subtitle_Message("$"..(9904000+index),900)',
            '    print("VR_GALLERY: view="..index)','end',
            'function Gallery_Group(index)','    Gallery_CurrentGroup=index','    Gallery_CurrentFaction=Gallery_GroupFactions[index]',
            '    Gallery_Current=Gallery_First[index]','    Gallery_Mode="group"',
            '    Camera_Interpolate("here","Gallery_Group"..index,0)','    Subtitle_Message("$"..(9906000+index),900)',
            '    print("VR_GALLERY: group="..index)','end',
            'function Gallery_Category(index)','    local group=Gallery_FactionGroups[Gallery_CurrentFaction][index]',
            '    if group~=nil then Gallery_Group(group) end','end',
            'function Gallery_Faction(index)','    Gallery_CurrentFaction=index','    Gallery_CurrentGroup=Gallery_FactionGroups[index][1]',
            '    Gallery_Current=Gallery_First[Gallery_CurrentGroup]','    Gallery_Mode="faction"',
            '    Camera_Interpolate("here","Gallery_Faction"..index,0)','    Subtitle_Message("$"..(9907000+index),900)',
            '    print("VR_GALLERY: faction="..index)','end',
            'function Gallery_FactionOverview()','    Gallery_Faction(Gallery_CurrentFaction)','end',
            'function Gallery_FocusFirst()','    Gallery_Show(Gallery_First[Gallery_CurrentGroup])','end',
            'function Gallery_Next()','    if Gallery_Mode~="pair" then Gallery_Show(Gallery_First[Gallery_CurrentGroup]); return end',
            '    local index=Gallery_Current+1','    if index>Gallery_Total then index=1 end','    Gallery_Show(index)','end',
            'function Gallery_Previous()','    if Gallery_Mode~="pair" then Gallery_Show(Gallery_Last[Gallery_CurrentGroup]); return end',
            '    local index=Gallery_Current-1','    if index<1 then index=Gallery_Total end','    Gallery_Show(index)','end',
            'function Gallery_NextGroup()','    local index=Gallery_CurrentGroup+1','    if index>Gallery_GroupTotal then index=1 end','    Gallery_Group(index)','end',
            'function Gallery_PreviousGroup()','    local index=Gallery_CurrentGroup-1','    if index<1 then index=Gallery_GroupTotal end','    Gallery_Group(index)','end',
            'function Gallery_Overview()','    Gallery_Mode="all"','    Camera_Interpolate("here","Gallery_Overview",0)',
            '    Subtitle_Message("$9904000",900)','    print("VR_GALLERY: overview")','end']
    for i in range(1,8):lua += [f'function Gallery_Class{i}()',f'    Gallery_Category({i})','end']
    for i in range(1,5):lua += [f'function Gallery_Faction{i}()',f'    Gallery_Faction({i})','end']
    (folder/'Inspect.lua').write_text('\n'.join(lua)+'\n',encoding='utf-8')


def write_docs(entries,groups,factions):
    text='# Компактная карта сравнения HWVR / HWRM\n\n'
    text+='`launch_test.ps1 -Gallery`. В парах HWVR слева, штатный HWRM справа. Автоувеличение с расстоянием отключено.\n\n'
    text+='Между аналогами — ширина большего корпуса; между соседними парами — сумма ширин соседних корпусов; между классами — длина большего корпуса. Совпадающие модели приведены к масштабу HWRM без растягивания по осям.\n\n'
    text+='F1 — Новокушане; F2 — Радаа; F3 — NPC; F4 — MISC.\n\n'
    text+='1–7 — обзор класса текущей фракции; N/P — отдельные пары; PgUp/PgDn — следующий/предыдущий класс. '
    text+='8 — обзор фракции; 9 — первая пара текущего класса; 0 — вся карта.\n\n'
    for faction in factions:
        text+=f'## {faction["name"]}\n\n'
        for i,group_id in enumerate(faction['groups'],1):
            group=groups[group_id-1];text+=f'### {i}. {group["name"]}\n\n| № | HWVR | HWRM |\n| --- | --- | --- |\n'
            for index in group['entries']:
                e=entries[index-1];text+=f'| {index} | {e["ru"]} | {e["native"] or "—"} |\n'
            text+='\n'
    Path('GALLERY.md').write_text(text,encoding='utf-8')
