"""Recover demo mission definitions, serialized scenario graphs and scene layouts."""

import json
import argparse
import re
import struct
from collections import Counter
from pathlib import Path

from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator
from UnityPy.helpers.TypeTreeNode import TypeTreeNode

from export_catalogue import Source


GAME=Path(r'C:\Program Files (x86)\Steam\steamapps\common\Homeworld Vast Reaches Demo')
OUT=Path('local/campaign-audit')
TYPE_TREE_GAME=GAME
QUEST_V110=False


def corrected_tree(node,qualified=None):
    """Correct generator string-array dispatch and MonoBehaviour header alignment.

    Fresh nodes are necessary: UnityPyBoost caches its read operations per node.
    Keep strict full-object byte consumption; never accept a partial spawner.
    """
    typ=node.m_Type
    array=next((c for c in node.m_Children if c.m_Type=='Array'),None)
    if typ=='string' and array and any(c.m_Name=='data' and c.m_Type=='string' for c in array.m_Children):typ='vector'
    flags=(node.m_MetaFlag or 0)|(0x4000 if node.m_Name=='m_Enabled' else 0)
    children=node.m_Children
    if QUEST_V110 and qualified=='Hercules.Designer.MissionDatabase':
        children=[c for c in children if c.m_Name!='_demoMissions']
    if QUEST_V110 and qualified=='Hercules.Designer.ObjectiveDefinition':
        children=[c for c in children if c.m_Name!='ModelScaleMultiplier']
    return TypeTreeNode(node.m_Level,typ,node.m_Name,node.m_ByteSize,node.m_Version,
                        m_Children=[corrected_tree(c,qualified) for c in children],m_MetaFlag=flags)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    source=Source(GAME/'HomeworldVastReachesDemo_Data')
    streaming=GAME/'HomeworldVastReachesDemo_Data/StreamingAssets/aa'
    bundles=streaming/('Android' if (streaming/'Android').is_dir() else 'StandaloneWindows64')
    for path in sorted(bundles.glob('*.bundle')):source.env.load_file(str(path))
    objects=list(source.env.objects)
    generator=TypeTreeGenerator('2021.3.38f1');generator.load_local_game(str(TYPE_TREE_GAME))
    source.env.typetree_generator=generator
    records=[];failures=[];counts=Counter();index={};files={};trees={}
    for obj in objects:
        af=obj.assets_file
        files.setdefault(af.name,dict(externals=[e.path.rsplit('/',1)[-1] for e in af.externals]))
        if obj.type.name=='MonoBehaviour':
            try:
                raw=obj.get_raw_data();file_id,path_id=struct.unpack_from('<iq',raw,16)
                script=source.resolve(dict(m_FileID=file_id,m_PathID=path_id),af)
                if not script:continue
                sd=source.read(script);assembly=sd['m_AssemblyName'];cls=sd['m_ClassName'];namespace=sd['m_Namespace']
                qualified=(namespace+'.' if namespace else '')+cls
                counts[(af.name,qualified)]+=1
                if not (assembly=='FarBridge.Hercules.dll' or assembly in ('Unity.VisualScripting.Flow.dll','Unity.VisualScripting.Core.dll','Unity.Timeline.dll','Unity.Localization.dll','AK.Wwise.Unity.Timeline.dll') or cls=='WwiseEventReference'):continue
                tree_key=(assembly,qualified)
                if tree_key not in trees:trees[tree_key]=corrected_tree(generator.get_nodes_up(assembly,qualified),qualified)
                data=obj.parse_as_dict(node=trees[tree_key])
                record=dict(source=af.name,path_id=obj.path_id,class_name=qualified,assembly=assembly,name=data.get('m_Name',''),data=data)
                records.append(record)
                index[(af.name,obj.path_id)]=record
            except Exception as exc:
                failures.append(dict(source=af.name,path_id=obj.path_id,class_name=locals().get('qualified'),error=str(exc)))
        elif obj.type.name in ('GameObject','Transform','RectTransform','Animator','AnimationClip','PlayableDirector'):
            try:
                data=source.read(obj)
                records.append(dict(source=af.name,path_id=obj.path_id,class_name=obj.type.name,name=data.get('m_Name',''),data=data))
            except Exception as exc:failures.append(dict(source=af.name,path_id=obj.path_id,error=str(exc)))
    for file_name in sorted({r['source'] for r in records}):
        rows=[r for r in records if r['source']==file_name]
        safe=re.sub(r'[^A-Za-z0-9._-]','_',file_name)
        (OUT/(safe+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    report=dict(records=len(records),files=files,failures=failures,
                mono_types=[dict(source=f,class_name=c,count=n) for (f,c),n in counts.most_common()])
    (OUT/'index.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Recovered records:',len(records),'read failures:',len(failures))
    for record in records:
        if any(s in record['class_name'] for s in ('MissionDefinition','MissionDatabase','ObjectiveDatabase','CutsceneDatabase','MissionDialogue','AbilityDefinition')):
            print(record['source'],record['path_id'],record['class_name'],record['name'])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game',type=Path,default=GAME)
    parser.add_argument('--output',type=Path,default=OUT)
    parser.add_argument('--type-tree-game',type=Path)
    parser.add_argument('--quest-v110',action='store_true',help='Older Quest layout: no demo array or objective model scale field; full-object reads remain strict.')
    args=parser.parse_args()
    GAME=args.game
    OUT=args.output
    TYPE_TREE_GAME=args.type_tree_game or GAME
    QUEST_V110=args.quest_v110
    main()
