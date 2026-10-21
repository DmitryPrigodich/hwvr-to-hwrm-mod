"""Two living mission dossiers: source, adaptation, EN/new RU/old RU and branches."""
import collections
import json
from pathlib import Path
import write_demo_scenarios as demo
import write_quest_progression as q

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/missions'

T1_FLOW='''flowchart TD
  P[Общий пролог] --> C[Первое подключение Тирры]
  C --> S[Сенсоры и упражнения навигации]
  S --> M{Группа прошла две зоны?}
  M -- нет --> M
  M -- да --> E[Создать учебную цель]
  E --> K{Цель уничтожена?}
  K -- нет --> K
  K -- да --> B[Диалог о потерях; урок постройки и редактирования]
  B --> G[Команды нескольким группам и маршрут]
  G --> F{Конечные цели уничтожены?}
  F -- да --> H[Первый гиперпрыжок; завершение T1]
  F -- нет --> F
'''
M1_FLOW='''flowchart TD
  A[Прибытие на полигон] --> R{Добыто суммарно 200 RU?}
  R -- нет --> R
  R -- да --> B[Построить разведчик]
  B --> S[Активным сканированием обнаружить патруль]
  S --> P1[Уничтожить patrolC]
  P1 --> P2[Уничтожить patrolB]
  P2 --> P3[Уничтожить patrolA]
  P3 --> T[Амма предъявляет договор; появляются фрегаты]
  T --> F{Ракетные фрегаты уничтожены?}
  F -- нет --> F
  F -- да --> X[Подкрепления Радаа; приказ отступить]
  X --> W[Гиперпрыжок и завершение]
  T -. параллельно .-> D{Порог урона Материнскому кораблю?}
  D -- 33 / 66 / 80 процентов --> V[Соответствующая тревога или диалог]
  V -. основная цель остаётся .-> F
  A -. независимый контроль потерь .-> Q{Сработало условие потери флота или Материнского корабля?}
  Q -- да --> L[Поражение]
'''


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    loc=json.loads((ROOT/'campaign-export/manifests/localization.json').read_text(encoding='utf8'))
    cues={r['key']:r for r in json.loads((ROOT/'campaign-export/manifests/dialogue.json').read_text(encoding='utf8'))}
    chars={r['id']:r for r in json.loads((ROOT/'campaign-export/manifests/characters.json').read_text(encoding='utf8'))}
    old_ru={k:v for t in json.loads((q.DATA/'strings-ru.json').read_text(encoding='utf8')).values() for k,v in t.items()}
    maps=json.loads((ROOT/'campaign-export/manifests/placements.json').read_text(encoding='utf8'))['missions']
    timings=json.loads((ROOT/'campaign-export/manifests/timelines.json').read_text(encoding='utf8'))
    index=json.loads((q.RAW/'index.json').read_text())
    for code in ['T1','M1']:
        m=next(m for m in q.MISSIONS if m['id']=='Mission_'+code);p=q.mission_info(m)
        definition=q.raw_file(m['source'])[m['path_id']]['data']
        title=loc[definition['_missionNameKey']]['ru']
        placement=next(s for s in maps if s['mission']==m['id'])
        directory=placement['directory'];folder=ROOT/'campaign-export/data/leveldata/campaign/VastReachesFull'/directory
        loading=ROOT/f'campaign-export/assets/loading/{m["id"]}.png'
        nodes=p['graph']['nodes'];by_key=collections.defaultdict(list)
        for n in nodes:
            d=n.get('resolved_objects',{}).get('_dialogueLine')
            if n['$type'].endswith('.PlayDialogue') and d:by_key[d['text_key']].append(n.get('$id','изолированный'))
        source_demo=json.loads((demo.DATA/f'Mission_{code}-graph.json').read_text(encoding='utf8'))
        demo_nodes={n['$id']:n for n in source_demo['nodes'] if '$id' in n}
        visited=set()
        lines=[f'# {code}. {title} — разбор миссии','',
            'Живой рабочий документ, 18 октября 2026 года. Здесь три слоя: **что есть в оригинале**, **что подготовлено для HWRM**, **что ещё согласовать**. Подробности будем дополнять в этом же файле. Английский и новый русский стоят рядом; старый русский спрятан под репликой для сравнения. Технические имена сейчас не переименовываем.','',
            f'Источник: полная Quest 1.1.0-16520, `{m["scene_file"]}` / `{m["main_scene"]}`. Используемые английские строки этой миссии совпадают со Steam-демкой. Числа ниже взяты из Quest; отличие уже установленной мини-демки отмечено отдельно.','',
            '## Материалы и готовность','',
            *(['21 октября: установлен [штатный путь речи и портретов](../CAMPAIGN_SPEECH.md): Subtitle_Add/Subtitle_IsDone, PCM WAV, actor-темы27–31. Для T1 четыре реплики, для M1 девятнадцать. Дмитрий подтвердил в игре пролог и диалоги с портретами начала T1; полное прохождение T1 и речь M1 ещё не подтверждены. Портреты слегка растянуты, косметическая правка отложена; речь вступлений вынесена из WebM в AddSpeechEvent.',''] if code in ('T1','M1') and (ROOT/'minicampaign/leveldata/campaign/VastReachesMiniCampaign/VRC_Speech.lua').exists() else []),
            *(['21 октября: [пролог](../PROLOGUE_CINEMATIC.md) установлен перед T1; повтор восьми вступительных строк убран. После исправления упаковки RU/EN восстановлены меню, после переноса речи из WebM пользователь подтвердил пролог, диалоги и портреты. Пропуск ролика отдельно не подтверждён; [статус и ограничения](../CAMPAIGN_SPEECH.md). В предыдущем нативном T1 журнал показал неудачные Player_GrantResearchOption для NKR_FighterChassis/NKR_FighterDrive и отсутствующие UCS9902002/9902003; это отдельные замечания проверки миссии. Далее пользователь читает обучение и готовит фидбэк.',''] if code == 'T1' else []),
            '| Часть | Извлечено / подготовлено | Что остаётся |','|---|---|---|',
            f'| Загрузка | [Исходная картинка](<{loading.as_posix()}>), DDS рядом с `.level` | Проверить отображение движком |',
            ('| Говорящие головы | Исходные PNG, TGA и speech actors; показ в начале T1 подтверждён | Позже исправить небольшое растяжение |' if code=='T1' else '| Говорящие головы | Исходные PNG, TGA и speech actors подключены | Проверить в M1; небольшое растяжение замечено в T1 |'),
            ('| Звуки и диалоги | EN, новый RU, старый RU; PCM/Speech и диалоги начала T1 подтверждены в игре | Проверить всю очередь при полном прохождении |' if code=='T1' else '| Звуки и диалоги | EN, новый RU, старый RU; PCM/Speech и 19 реплик подключены | Проверить очередь M1 в движке |'),
            '| Камеры и действия | Timeline-клипы и узлы графа, ID и связи | Постановка HWRM/NIS, замена VR-управления |',
            f'| Карта | [Подготовленная .level](<{(folder/(directory+".level")).as_posix()}>), области и маршруты | Выбрать и адаптировать орбитальную сцену Хиигары HWRM |',
            '| Наш флот и стройка | Составы, RU, whitelist, исходные открытия | Эскадрильи, зависимости HWRM и правила переноса флота |',
            '| Враг / нейтралы | Стартовые размещения и отдельные отложенные шаблоны | Условия появления, повторы волн, поведение |','',
            f'![Изображение главы](<{loading.as_posix()}>)','',
            '## Карта: переиспользуем HWRM по смыслу','',
            'Для этой главы выбираем готовое окружение Хиигары: первый кандидат — **HW2 Remastered, M02_Hiigara**, дополнительно можно сравнить орбиту Хиигары из финала HW1. Берём планету, фон и подходящие декорации; вражеский сценарий исходной миссии HWRM не копируем. Нужные VR-зоны обнаружения, маршруты и дистанции восстанавливаем под наши события. Готовая `.level` сейчас служит измерительной базой, а не обязательством перенести каждый астероид. Конкретное окружение ещё не заменено и требует визуальной сверки вместе.','',
            '## Наш стартовый флот, ресурсы и ограничения','',
            f'Начальные параметры оригинала: **{m["starting_ru"]} RU**, лимит **{m["fleet_cap"]} отрядов**, Carryover = **{m["carryover"]}**. False здесь означает заданный старт этой главы в источнике, а не запрет HWRM переносить флот вообще.','',
            '| Группа | Состав исходника | Отрядов / физических корпусов |','|---|---|---|']
        for group in p['fleet']:lines.append(f'| `{group["name"]}` ({group["kind"]}) | {q.composition(group["counts"],technical=False)} | {q.total_counts(group["counts"])} |')
        lines+=['',f'Итого baseline: **{q.total_counts(p["total"])}**. Столбцы — отряды / корпуса, это разные числа.','',
            '| Разрешено строить в исходнике | RU | Время боя, с |','|---|---:|---:|']
        for b in p['available']:
            d=b['data'];lines.append(f'| {q.ship_name(d["_shipType"],technical=False)} (`{b["name"]}`) | {d["_cost"]} | {d["_duration"]:g} |')
        lines+=['',f'Контроллер: **{p["mode"]}**. Перечисленные цены/время принадлежат VR, это ещё не выбранный баланс HWRM. Отдельной платной очереди исследований в этой главе не найдено. Разрешение строительства, учебная блокировка интерфейса и оплачиваемое исследование — разные вещи.','']
        if code=='T1':lines+=['В T1 строится только перехватчик. Сценарий выдаёт ещё **1000 RU** во время урока тактической паузы. Два появления учебных StrikeGroupA/B дают по три отряда перехватчиков — по **15 физических корпусов**. Это не стартовый флот. Установленная мини-демка пока использует сокращённое упражнение и заранее размещённые одиночные Kushan; полный экспорт T1 начинает с одного Материнского корабля, как исходник.','']
        else:lines+=['В M1 задача добычи **200 RU суммарно** не открывает новое исследование: четыре типа уже разрешены контроллером. Затем нужны постройка разведчика и обнаружение патруля. В установленной мини-демке старт пока **9 физических корпусов вместо 37**; в полном экспорте развёрнут исходный SquadronCount. Нативное число тел/эскадрилий ещё проверим движком.','']
        chapter_keys=set(by_key)
        if code=='T1':
            chapter_keys.update(c['key'] for t in timings for c in t['clips'] if any(x['key']=='M01_010_010_A_HA' for x in t['clips']))
        speaker_keys=collections.defaultdict(set)
        for key in chapter_keys:
            for cid in cues[key]['character_ids']:speaker_keys[cid].add(key)
        lines+=['## Говорящие головы и звук этой главы','',
                '| Говорящий | Исходный портрет | Ключей реплик / звуков |','|---|---|---|']
        for cid,keys in speaker_keys.items():
            c=chars[cid];picture=c['portrait']
            link='[PNG](<'+(ROOT/'campaign-export'/picture['path']).as_posix()+'>)' if picture else 'В источнике портрета нет'
            lines.append(f'| {c["ru"]} | {link} | {len(keys)} / {sum(bool(cues[k]["english_audio"]) for k in keys)} |')
        lines+=['','Для каждого ключа ниже есть ссылка на WAV. Имена и суффиксы звуковых файлов не определяют говорящего: использована фактическая цепочка Character → DialogueLine → WwiseEvent → MediaRef. Это оригинальная английская озвучка; новый русский — текст субтитров.','',
            '## Схема событий: что последовательно, а что параллельно','',
            'Сплошные стрелки — основная цепочка, ромбы — условия. Пунктир — отдельный обработчик, который работает параллельно цепочке. Тревога от урона может прозвучать во время любой текущей задачи; она не означает, что следующая напечатанная реплика уже обязана начаться.','',
            '```mermaid',T1_FLOW if code=='T1' else M1_FLOW,'```','',
            '## Вражеские / дружеские появления','',
            'Ниже подключённые SpawnEntity, а не все шаблоны, лежащие на карте. Состав показан за одно срабатывание; PatrolManager может выбирать вариант и повторяться. Название редакторской группы — ориентир, реальные условия основного маршрута показаны в схеме и сценах диалога.','',
            '| Узел / группа редактора | Создаваемая цель | Состав и сторона источника |','|---|---|---|']
        for n in nodes:
            if not n['$type'].endswith('.SpawnEntity'):continue
            for alias,target in q.spawn_targets(p['graph'],p['scene'],n):
                body=q.spawner_description(target).replace('|','/').replace('\n',' ')
                lines.append(f'| `{n.get("$id","?")}` / {q.group_label(p["graph"],n)} | `{alias}` → `{target["name"]}` | {body} |')
        lines+=['','Источник TeamId: **1 — игрок, 1024 — Радаа, 0 — нейтральный**, 2048 — дополнительная компьютерная сторона. Для тренировочных целей действуют свои ограничения активности/уязвимости. Количество автоматически размещённых исходных групп: '+str(len(p['auto']))+'.','',
            '## Камеры и действия','', '[Родное обучение HWRM и сопоставление с VR](../HWRM_NATIVE_TUTORIAL.md): подготовлены отдельные разборы трёх стандартных уроков, исходные реплики и голос. Отсюда берём проверенные упражнения с мышью/клавиатурой, сохраняя сюжетные разговоры VR.','',
            'В игровом графе VR нет готового NIS для HWRM. Управление восприятием/камерой часто задано режимом сенсоров и уроками контроллеров; вступление использует отдельную Unity Timeline. Ниже сохранены управляющие действия для адаптации, а не заявлено готовое движение камеры HWRM.','',
            '| Тип узла | ID | Дальнейшая адаптация |','|---|---|---|']
        kinds={'SetSensorsManagerDisplayMode':'Режим сенсоров/фокус; подобрать штатную камеру HWRM.','BeginLesson':'Заменить VR-урок обучением камере, приказам и строительству HWRM.','WaitForLessonCompleted':'Реальное условие завершения упражнения, не просто задержка.','HyperspaceWarp':'Штатный/сценарный гиперпрыжок и переход.','ModifyHealth':'Сюжетный урон; сохранить порог и причину.','SetMoveTarget':'Приказ движения к нужной зоне.','SetAttackTarget':'Приказ атаки нужной стороны.','LockControls':'Ограничение управления во время постановки.','UnlockControls':'Вернуть управление.'}
        for kind,note in kinds.items():
            ids=[n.get('$id','изолированный') for n in nodes if n['$type'].endswith('.'+kind)]
            if ids:lines.append(f'| {kind} | '+', '.join('`'+i+'`' for i in ids)+' | '+note+' |')
        lines+=['','## Сцены и переводы','']
        def quote(key,tag='Реплика'):
            assert key in loc,key
            v=loc[key];cue=cues.get(key);speaker=tag
            if cue and len(cue['character_ids'])==1:speaker=chars[cue['character_ids'][0]]['ru']
            out=[f'**{speaker}** — `{key}`','', '**EN:** '+v['en'],'','**RU, новый:** '+v['ru'],'', '<details><summary>Старый русский перевод для сравнения</summary>','',old_ru.get(key,'Нет строки в исходной таблице.'),'','</details>','']
            if cue and cue.get('english_audio'):out+=['[Исходный звук](<'+(ROOT/'campaign-export'/cue['english_audio']['wav']).as_posix()+'>)','']
            return out
        if code=='T1':
            prologue=next(t for t in timings if any(c['key']=='M01_010_010_A_HA' for c in t['clips']))
            lines+=['### Пролог — перед обучением','', 'Общий сюжетный пролог теперь показан здесь один раз; в M1 он повторно не печатается.','']
            for clip in prologue['clips']:lines += [f'*Timeline: {clip["start"]:.2f} с, длительность клипа {clip["duration"]:.2f} с.*','']+quote(clip['key'])
        else:lines+=['Общий пролог вынесен в [разбор T1](T01_Training.md). Здесь начинаем с прибытия на полигон.','']
        for heading,context,ids,tasks in demo.STAGES[code]:
            lines+=['### '+heading,'',context.replace('Гитан','Гиитан'),'']
            for ident in ids:
                key=demo_nodes[str(ident)]['resolved_objects']['_dialogueLine']['text_key']
                if key in visited:continue
                assert key in by_key,(code,key)
                visited.add(key);lines+=quote(key)
                lines+=['*Quest PlayDialogue: '+', '.join(by_key[key])+'.*','']
            for key in tasks:lines+=quote(key,'Задача')
        assert visited==set(by_key),(code,set(by_key)-visited)
        lines+=['## Следующие решения и журнал','',
            '- [x] Новый RU и EN вынесены в отдельный файл миссии; старый RU оставлен для сверки.',
            '- [x] Гиитан и Тварь приведены к принятой терминологии в новом переводе.',
            '- [x] Составы и появления отделены от стартового флота; добавлена схема условий.',
            '- [ ] Дмитрий сверяет реплики и глоссарий; фиксируем правки здесь.',
            '- [ ] Утвердить окружение Хиигары из HWRM и нужные области сценария.',
            '- [ ] Проверить эскадрильи, RU, стройку, камеры и все реальные условия движком.',
            '- [ ] Подключить WAV-речь/портреты и проверить темп диалога.',
            '- [ ] Зафиксировать правила перехода и переноса флота. В оригинале T1/M1 имеют заданные старты; переносить всё автоматически поверх них нельзя.',
            '', 'Полные источники и оставшиеся обработчики: [QUEST_PROGRESSION.md](../QUEST_PROGRESSION.md), [CAMPAIGN_EXPORT_SCRIPTS.md](../CAMPAIGN_EXPORT_SCRIPTS.md), `campaign-export/manifests/placements.json`. Проверка игры в этом заходе не выполнялась.','']
        path=OUT/(directory+'.md');path.write_text('\n'.join(lines),encoding='utf8')
        print(json.dumps({'file':str(path),'graph_dialogue_keys':len(visited),'bytes':path.stat().st_size},ensure_ascii=False))


if __name__=='__main__':main()
