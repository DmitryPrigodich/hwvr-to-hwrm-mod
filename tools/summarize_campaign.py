"""Resolve the recovered demo scenario assets into reusable campaign data."""

import json
import argparse
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from export_ship import rotate


RAW=Path('local/campaign-audit')
OUT=Path('local/campaign')
GAME=Path(r'C:\Program Files (x86)\Steam\steamapps\common\Homeworld Vast Reaches Demo')
QUEST=False


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    info=json.loads((RAW/'index.json').read_text(encoding='utf-8'))
    records=[]
    for name in info['files']:
        path=RAW/(re.sub(r'[^A-Za-z0-9._-]','_',name)+'.json')
        if path.exists():records.extend(json.loads(path.read_text(encoding='utf-8')))
    index={(r['source'],r['path_id']):r for r in records}
    def write(name,data):
        (OUT/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    def resolve(owner,ref):
        if not ref or not ref.get('m_PathID'):return None
        file=owner['source'];external=ref.get('m_FileID',0)
        if external:file=info['files'][file]['externals'][external-1]
        return index.get((file,ref['m_PathID']))
    def go(record):
        return resolve(record,record['data'].get('m_GameObject')) if record else None
    def label(record):
        if not record:return None
        gameobject=go(record)
        return record.get('name') or (gameobject or {}).get('name') or record['class_name']
    def describe(record):
        if not record:return None
        return dict(source=record['source'],path_id=record['path_id'],class_name=record['class_name'],name=label(record))
    def transform(record):
        gameobject=record if record['class_name']=='GameObject' else go(record)
        if not gameobject:return None
        for c in gameobject['data']['m_Component']:
            item=resolve(gameobject,c['component'])
            if item and item['class_name']=='Transform':return item
    def point_in_world(tr,point=(0,0,0)):
        seen=set()
        while tr:
            key=(tr['source'],tr['path_id'])
            if key in seen:raise ValueError('Cyclic scene transform')
            seen.add(key);data=tr['data']
            point=rotate(tuple(v*data['m_LocalScale'][a] for v,a in zip(point,'xyz')),data['m_LocalRotation'])
            point=tuple(v+data['m_LocalPosition'][a] for v,a in zip(point,'xyz'))
            tr=resolve(tr,data.get('m_Father'))
        return point
    shared={r['data']['m_TableCollectionName']:{e['m_Id']:e['m_Key'] for e in r['data']['m_Entries']}
            for r in records if r['class_name'].endswith('.SharedTableData')}
    localization={}
    for record in records:
        if not record['class_name'].endswith('.StringTable'):continue
        data=record['data'];lang=data['m_LocaleId']['m_Code'];table=record['name'].rsplit('_',1)[0]
        keys=shared[table]
        localization.setdefault(lang,{})[table]={keys.get(e['m_Id'],str(e['m_Id'])):e['m_Localized'] for e in data['m_TableData']}
    for lang in ('en','ru'):write('strings-'+lang,localization[lang])
    english=localization['en'];russian=localization['ru']
    def text(key,table='Strings_Missions'):
        return dict(en=english[table].get(key),ru=russian[table].get(key))
    ship_names={r['data']['_staticData']['<Type>k__BackingField']:r['name'] for r in records if r['class_name']=='Hercules.Designer.ShipDefinition'}
    def group(record):
        if not record:return None
        data=record['data'].get('_data',{})
        result={**describe(record), 'auto_spawn':record['data'].get('_autoSpawn'), 'data':data}
        members=data.get('Members',[])
        if 'Type' in data:members=[dict(Type=data['Type'])]
        result['members']=[dict(m,ship_definition=ship_names.get(m['Type'])) for m in members]
        unique=resolve(record,data.get('UniqueMember'))
        if unique:result['unique_member']=group(unique)
        tr=transform(record)
        if tr:result['world_position']=point_in_world(tr)
        return result
    if QUEST:
        import UnityPy
        env=UnityPy.load(str(GAME/'HomeworldVastReachesDemo_Data/globalgamemanagers'))
        settings=next(o.parse_as_dict()['scenes'] for o in env.objects if o.type.name=='BuildSettings')
    else:
        settings=json.loads(Path('local/demo-audit.json').read_text(encoding='utf-8'))['scenes'][0]['scenes']
    built={name:'level'+str(i) for i,name in enumerate(settings)}
    database=next(r for r in records if r['class_name']=='Hercules.Designer.MissionDatabase')
    missions=[]
    for category in ('_demoMissions','_campaignMissions','_challengeMissions','_tutorialMissions'):
        for order,ref in enumerate(database['data'].get(category,[]),1):
            record=resolve(database,ref);data=record['data']
            mission=dict(category=category,order=order,id=record['name'],**describe(record))
            mission.update(title=text(data['_missionNameKey']),description=text(data['_missionDescriptionKey']),
                           main_scene=data['_mainScene']['_path'],scene_file=built.get(data['_mainScene']['_path']),
                           intro_scene=data['_introScene']['_path'],intro_present=data['_introScene']['_path'] in built,
                           starting_ru=data['DefaultRU'],fleet_cap=data['<FleetCap>k__BackingField'],carryover=bool(data['<AllowCarryover>k__BackingField']),
                           default_groups=[group(resolve(record,r)) for r in data['DefaultGroups']],
                           additional_groups=[group(resolve(record,r)) for r in data['<AdditionalGroups>k__BackingField']])
            missions.append(mission)
    write('missions',missions)
    scenes=[]
    scene_numbers=[i for i,n in enumerate(settings) if ('/M' in n or '/Tutorials/' in n) and not any(s in n for s in ('Lighting','_Animatic_','/Core/'))] if QUEST else [1,4,6,9]
    for number in scene_numbers:
        name='level'+str(number);rows=[r for r in records if r['source']==name]
        placements=[];areas=[];routes=[];loadouts=[];build=[];variables=[];controllers=[]
        for record in rows:
            cls=record['class_name'];data=record['data']
            if cls.endswith(('GroupSpawner','SquadronSpawner','PropSpawner','TaggedSpawnPoint','DetectionSphere','VisionSphereInitializer','MapCoordinates','LoadoutSpawner','Route','PatrolManager')):
                value={**describe(record),'data':data}
                tr=transform(record)
                if tr:value['world_position']=point_in_world(tr)
                if cls.endswith(('GroupSpawner','SquadronSpawner')):value.update(group(record))
                if cls.endswith('Spawner') or cls.endswith('SpawnPoint'):placements.append(value)
                elif cls.endswith(('Route','PatrolManager')):routes.append(value)
                else:areas.append(value)
                if cls.endswith('LoadoutSpawner'):
                    loadouts.append(dict(spawn_positions=[dict(reference=r,world_position=point_in_world(resolve(record,r)))
                                                          for r in data.get('<SpawnPositions>k__BackingField',[])]))
            if cls.endswith('BuildCommandController'):
                controllers.append(dict(owner=describe(record),mode=data.get('_controlMode'),data=data))
                for ref in data['_buildCommandList']['_buildCommands']:
                    target=resolve(record,ref);build.append(dict(definition=describe(target),data=target['data'] if target else None))
            if cls=='Unity.VisualScripting.Variables':
                serialized=data['_data'];values=json.loads(serialized['_json'])
                variables.append(dict(owner=describe(record),values=values,
                                      object_references=[describe(resolve(record,r)) for r in serialized['_objectReferences']]))
        scene=dict(scene_file=name,unity_scene=settings[number],placements=placements,areas=areas,routes=routes,loadout_positions=loadouts,
                   build_commands=build,build_controllers=controllers,variables=variables)
        write(name,scene);scenes.append(dict(scene_file=name,placements=len(placements),routes=len(routes),areas=len(areas),
                                           build_commands=[b['definition']['name'] for b in build if b['definition']]))
    graphs=[]
    for record in records:
        if record['class_name']!='Unity.VisualScripting.ScriptGraphAsset':continue
        data=record['data']['_data'];graph=json.loads(data['_json'])['graph'];elements=graph['elements']
        references=[resolve(record,r) for r in data['_objectReferences']]
        nodes=[];edges=[]
        for element in elements:
            if element['$type'].endswith(('ControlConnection','ValueConnection')):edges.append(element);continue
            node=dict(element);node['resolved_objects']={}
            for key,value in element.get('defaultValues',{}).items():
                if isinstance(value,dict) and value.get('$type')=='UnityEngine.Object':
                    target=references[value['$content']];detail=describe(target)
                    if target:
                        td=target['data'];key2=td.get('_textKey') or td.get('StaticData',{}).get('LocalizationKey')
                        if key2:detail.update(text_key=key2,text=text(key2))
                    node['resolved_objects'][key]=detail
            nodes.append(node)
        write(record['name']+'-graph',dict(source=describe(record),nodes=nodes,edges=edges,
                                        object_references=[describe(r) for r in references],variables=graph.get('variables')))
        graphs.append(dict(name=record['name'],nodes=len(nodes),edges=len(edges),
                           control_edges=sum(e['$type'].endswith('ControlConnection') for e in edges),
                           labels=[e.get('label') for e in elements if e['$type'].endswith('GraphGroup')]))
    abilities=[]
    for record in records:
        if record['class_name']!='Hercules.AbilityDefinition':continue
        data=record['data'];abilities.append(dict(id=record['name'],name=text(data['_nameKey'],'Strings_ShipInfo'),
                                                 description=text(data['_descriptionKey'],'Strings_ShipInfo'),data=data['_staticData'],ships=[]))
        for ship in records:
            if ship['class_name']!='Hercules.Designer.ShipDefinition':continue
            for ability in ship['data'].get('_shipAbilities',[]):
                if resolve(ship,ability['Definition'])==record:abilities[-1]['ships'].append(ship['name'])
    write('abilities',abilities)
    audio_root=GAME/'HomeworldVastReachesDemo_Data/StreamingAssets/Audio/GeneratedSoundBanks/Windows'
    tree=ET.parse(audio_root/'SoundbanksInfo.xml');audio=[]
    actual={p.stem:p for p in audio_root.rglob('*.wem')}
    for element in tree.iter('File'):
        name=element.findtext('ShortName') or '';ident=element.get('Id');path=actual.get(ident)
        audio.append(dict(id=ident,name=name,language=element.get('Language'),
                          present=bool(path),path=str(path) if path else None))
    write('audio-index',audio)
    narrative=[a for a in audio if re.match(r'(M\d+|T\d+|C\d+)',a['name'])]
    voice_by_name={Path(a['name']).stem:a for a in narrative}
    for table in ('Strings_Missions','Strings_Animatics'):
        values=[dict(key=key,**text(key,table),voice=voice_by_name.get(key)) for key in english[table]]
        write('transcript-'+table.removeprefix('Strings_').lower(),values)
    summary=dict(raw_records=len(records),read_failures=info['failures'],languages=sorted(localization),
                 english_tables={k:len(v) for k,v in english.items()},scenes=scenes,graphs=graphs,
                 campaign_definitions=sum(m['category']=='_campaignMissions' for m in missions),
                 built_scenes=settings,audio_files_indexed=len(audio),audio_files_present=sum(a['present'] for a in audio),
                 narrative_audio_files=len(narrative),narrative_audio_present=sum(a['present'] for a in narrative),
                 narrative_audio_by_prefix=dict(Counter(re.match(r'(M\d+|T\d+|C\d+)',a['name'])[1] for a in narrative)),abilities=len(abilities))
    write('summary',summary)
    print(json.dumps({k:v for k,v in summary.items() if k not in ('graphs','built_scenes','read_failures')},ensure_ascii=False,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game',type=Path,default=GAME)
    parser.add_argument('--raw',type=Path,default=RAW)
    parser.add_argument('--output',type=Path,default=OUT)
    parser.add_argument('--quest',action='store_true')
    args=parser.parse_args()
    GAME=args.game;RAW=args.raw;OUT=args.output;QUEST=args.quest
    main()
