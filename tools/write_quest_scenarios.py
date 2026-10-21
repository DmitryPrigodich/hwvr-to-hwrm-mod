"""Readable EN/RU conversations and Timeline captions from the supplied Quest build.

Control edges establish order inside conversations. Independent event handlers are
kept as separate sections; localization key order is not treated as execution proof.
"""
import collections
import json
import re
import sys
from pathlib import Path
from campaign_text_review import review_label

ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/'local/quest-campaign'
RAW=ROOT/'local/quest-audit'


def main():
    literal='--raw' in sys.argv
    meta=json.loads((RAW/'index.json').read_text())
    cache={}
    def rows(name):
        if name not in cache:
            p=RAW/(name+'.json')
            cache[name]={r['path_id']:r for r in json.loads(p.read_text(encoding='utf8'))} if p.exists() else {}
        return cache[name]
    def ptr(owner,ref):
        if not ref or not ref.get('m_PathID'):return None
        source=owner['source']
        if ref.get('m_FileID'):source=meta['files'][source]['externals'][ref['m_FileID']-1]
        return rows(source).get(ref['m_PathID'])
    strings={}
    for lang in ['en','ru']:
        tables=json.loads((DATA/('strings-'+lang+'.json')).read_text(encoding='utf8'))
        strings[lang]={k:v for table in tables.values() for k,v in table.items()}
    if not literal:
        strings['ru'].update(json.loads((ROOT/'localization/ru/campaign.json').read_text(encoding='utf8')))
    def quoted(key):
        result=[f'`{key}`','']
        for lang in (['en','ru'] if literal else ['ru','en']):
            text=strings[lang].get(key)
            result += [lang.upper()+':','', '> '+text.replace('\n','\n> ') if text else '*Нет строки в извлечённой таблице этой версии.*','']
            if lang=='ru' and not literal and text:
                label=review_label(key,text)
                if label:result+=['*'+label+'*','']
        return result
    missions=json.loads((DATA/'missions.json').read_text(encoding='utf8'))
    built=json.loads((DATA/'summary.json').read_text())['built_scenes']
    allrows=[r for name in meta['files'] for r in rows(name).values()]
    definitions={r['name']:r for r in allrows if r['class_name']=='Hercules.MissionDefinition'}
    from campaign_cinematic_sources import scan_scenes
    _, cinematic_scenes = scan_scenes()
    cinematic_captions = {entry['scene']: [(clip['start'],clip['key']) for clip in entry['clips'] if not clip['effectively_muted']] for entry in cinematic_scenes}
    def captions(scene):
        return sorted(set(cinematic_captions.get(scene, [])))
    def event_label(node):
        label=node['$type'].rsplit('.',1)[-1]
        vals=node.get('defaultValues',{})
        details=[]
        for k,v in vals.items():
            if isinstance(v,dict) and isinstance(v.get('$content'),(str,int,float)) and v['$content']!='':details.append(k+'='+str(v['$content']))
        for v in node.get('resolved_objects',{}).values():
            if v:details.append(v.get('text_key') or v.get('name') or v['class_name'])
        return label+(' ('+', '.join(details)+')' if details else '')+' #'+node['$id']
    def graph_sections(graph):
        nodes={n.get('$id','unlinked_'+str(i)):dict(n,**{'$id':n.get('$id','unlinked_'+str(i))}) for i,n in enumerate(graph['nodes'])}
        forward=collections.defaultdict(list);backward=collections.defaultdict(list)
        for e in graph['edges']:
            if not e['$type'].endswith('ControlConnection'):continue
            a,b=e['sourceUnit']['$ref'],e['destinationUnit']['$ref']
            forward[a].append(b);backward[b].append(a)
        dialogue={n['$id']:n for n in nodes.values() if n['$type'].endswith('.PlayDialogue')}
        def key(ident):return dialogue[ident].get('resolved_objects',{}).get('_dialogueLine',{}).get('text_key')
        assert all(key(i) for i in dialogue),'Unresolved dialogue in '+graph['source']['name']
        def neighbours(start,links,stops):
            pending=list(links[start]);seen={start};found=[]
            while pending:
                ident=pending.pop(0)
                if ident in seen:continue
                seen.add(ident)
                if ident in stops:found.append(ident)
                else:pending+=links[ident]
            return found
        successors={i:neighbours(i,forward,dialogue) for i in dialogue}
        def stable_order(ident):return (key(ident),not ident.isdigit(),int(ident) if ident.isdigit() else ident)
        phases=collections.defaultdict(list)
        for i in dialogue:
            m=re.match(r'((?:M\d+|T\d+)_\d{3})_',key(i))
            phases[m[1] if m else 'Событийные и общие сообщения'].append(i)
        result=[]
        for phase,ids in sorted(phases.items()):
            ids=set(ids);incoming={i:0 for i in ids}
            for i in ids:
                for j in successors[i]:
                    if j in ids:incoming[j]+=1
            ready=sorted((i for i in ids if incoming[i]==0),key=stable_order)
            order=[];branch=len(ready)>1
            while ready:
                i=ready.pop(0);order.append(i)
                nexts=[j for j in successors[i] if j in ids]
                branch=branch or len(nexts)>1
                for j in nexts:
                    incoming[j]-=1
                    if incoming[j]==0:ready.append(j)
            # Cyclic/event-only fragments are listed explicitly, never guessed into a linear scene.
            leftover=ids-set(order)
            order+=sorted(leftover,key=stable_order)
            events={n['$id']:n for n in nodes.values() if n['$type'].rsplit('.',1)[-1].startswith('On') or n['$type'].endswith('.CustomEvent')}
            triggers=set()
            for i in order:
                triggers.update(event_label(events[j]) for j in neighbours(i,backward,events))
            result.append((phase,order,branch or bool(leftover),sorted(triggers)))
        return result,dialogue,key

    lines=['# Vast Reaches: сценарий кампании на русском и английском','',
           'Источник: предоставленные APK/OBB **1.1.0-16520**, без запуска игры. Это отдельная, более ранняя версия, а не дополнение к Steam-демке той же ревизии. В ней найдены 11 игровых миссий кампании, отдельное обучение, вступления и финальная сцена. Бонуса C1 в списке сцен этой сборки нет.','',
           ('Ниже буквальные EN/RU исходной локализации, включая её ошибки.' if literal else 'Русский текст заново переведён с английского оригинала с учётом сюжета, говорящих и терминологии Homeworld. Рядом сохранён английский оригинал; плохая исходная русская локализация доступна отдельно в [QUEST_SCENARIOS_RAW.md](archive/source-localization/QUEST_SCENARIOS_RAW.md). Перевод не добавляет новых сюжетных событий, исследований или реплик.')+' Состав флота, постройка и сюжетные открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md); сравнение ресурсов — в [QUEST_COMPARISON.md](QUEST_COMPARISON.md).','',
           'Порядок глав взят из MissionDatabase, он отличается от номеров внутренних M-файлов. Беседы сгруппированы по сценам диалога, а порядок реплик внутри связан управляющими рёбрами графа. **Независимые обработчики событий и развилки не образуют одну обязательную цепочку**: условия и ID узлов приведены рядом. Нумерация ключей используется для именования бесед, а не как доказательство очередности игры. Вступления упорядочены по времени клипов Timeline.','',
           'FI — разведка флота; TS — Тирра Собан; KS — Каран С’Джет; AR — Амма; GR — Гиитан. Смысл HA зависит от сцены: во вступлении M1 это рассказчик, в репликах верфи — её главный инженер.','']
    campaign=[m for m in missions if m['category']=='_campaignMissions']
    tutorial=[m for m in missions if m['category']=='_tutorialMissions']
    total=0;intro_count=0;output_index=[];seen_scenes=set()
    for mi,m in enumerate(tutorial+campaign,1):
        code=m['id'].removeprefix('Mission_')
        definition=definitions[m['id']]['data']
        title=strings['ru'].get(definition['_missionNameKey'],m['title']['ru'])
        label='Обучение' if code=='T1' else str(m['order'])
        heading='M0. Обучение / Tutorial' if code=='T1' and not literal else f'{label}. {code}: {title} / {m["title"]["en"]}'
        lines += [f'## {heading}','',
                  f'Определение `{m["source"]}:{m["path_id"]}`, карта `{m["scene_file"]}`. Подробные составы и открытия — в [QUEST_PROGRESSION.md](QUEST_PROGRESSION.md).','']
        for label,scene in [('Вступление',m['intro_scene']),('Финальная постановочная сцена',definitions[m['id']]['data'].get('_outroScene',{}).get('_path'))]:
            if scene and scene in seen_scenes:
                lines += ['Общий пролог уже приведён перед обучением; повторно не воспроизводится.',''];continue
            clips=captions(scene)
            if clips:
                seen_scenes.add(scene)
                lines += ['### '+label,'',f'`{scene}`','']
                for time,key in clips:
                    lines += [f'*Клип начинается в {time:.2f} с.*','']+quoted(key)
                intro_count+=len(clips)
        graph_name='Mission_M9_v2' if code=='M9' else m['id']
        path=DATA/(graph_name+'-graph.json')
        graph=json.loads(path.read_text(encoding='utf8'))
        sections,dialogue,key=graph_sections(graph)
        objectives={}
        for node in graph['nodes']:
            for obj in node.get('resolved_objects',{}).values():
                if obj and obj.get('class_name','').endswith('ObjectiveDefinition') and obj.get('text_key'):
                    objectives.setdefault(obj['text_key'],set()).add(node.get('$id','unlinked_'+node.get('guid','unknown')))
        lines += ['### Задачи, подключённые к графу','']
        for k,ids in sorted(objectives.items()):lines += [f'Узлы: {", ".join(sorted(ids,key=lambda s:(not s.isdigit(),int(s) if s.isdigit() else s)))}.','']+quoted(k)
        seen=set();key_list=[]
        for phase,order,branch,triggers in sections:
            lines += ['### '+phase,'']
            if triggers:lines += ['Обработчики, достигающие этих реплик по control-связям: '+ '; '.join('`'+t+'`' for t in triggers)+'.','']
            if branch:lines += ['*Есть независимые ветви: соседство абзацев не означает обязательное последовательное произнесение всех строк.*','']
            for i in order:
                k=key(i)
                if k in seen:continue
                seen.add(k);key_list.append(k)
                matching=sorted((node for node in dialogue if key(node)==k),key=lambda node:(not node.isdigit(),int(node) if node.isdigit() else node))
                references=', '.join('`'+graph_name+'#'+node+'`' for node in matching)
                lines += [('Узел ' if len(matching)==1 else 'Узлы ')+references+'.','']+quoted(k)
                if i.startswith('unlinked_'):lines += ['*Изолированный узел без ID/control-подключения: наличие текста не подтверждает его произнесение в игре.*','']
        assert seen=={key(i) for i in dialogue},m['id']
        total+=len(seen)
        output_index.append({'mission':m['id'],'graph':graph_name,'dialogue_keys':key_list,'objectives':list(objectives)})
    failures=collections.Counter(r.get('class_name','unknown') for r in meta['failures'])
    lines += ['## Полнота и ограничения','',f'Включено **{total} уникальных внутри глав реплик графов** и **{intro_count} реплик клипов вступлений/финала**. Повторяющиеся общие тревоги могут встречаться в нескольких главах. Покрытие всех найденных PlayDialogue проверено автоматически.','',
              'При чтении старой версии использована схема Steam с двумя проверенными отличиями: у MissionDatabase отсутствует массив демо-миссий, у ObjectiveStaticData — поле ModelScaleMultiplier. Разбор каждого сохранённого объекта требует полного совпадения длины, частичные чтения не принимаются. Все определения миссий, кораблей, задач и найденные сценарные графы прочитаны.','',
              f'Не прочитано {len(meta["failures"])} объектов, преимущественно HUD/UI/VFX старой версии. В том числе 9 AbilityDefinition несовместимы с новой схемой; их параметры в этом отчёте не реконструированы. Это ограничение аудита способностей, а не отсутствие девяти способностей в Quest. Полный список — local/quest-audit/index.json.','',
              'Проверка относится к данным и связям скриптов. Видимость реплик, тайминги, бой и все условия полного прохождения запуском не проверены. Наличие вступления не означает готовый видеоролик для HWRM: исходник использует Timeline/Unity и внешний звук.','']
    target=ROOT/('docs/archive/source-localization/QUEST_SCENARIOS_RAW.md' if literal else 'docs/QUEST_SCENARIOS.md')
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text('\n'.join(lines)+'\n',encoding='utf8')
    if not literal:(DATA/'scenario-coverage.json').write_text(json.dumps({'mission_dialogue_count':total,'timeline_dialogue_count':intro_count,'chapters':output_index},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'chapters':len(output_index),'mission_dialogues':total,'timeline_dialogues':intro_count,'bytes':target.stat().st_size}))


if __name__=='__main__':main()
