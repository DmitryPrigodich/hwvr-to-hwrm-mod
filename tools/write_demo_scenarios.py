"""Render an auditable reading edition of the three demo mission graphs.

Chapter order is authored from the graph's control connections, event handlers,
and objective transitions. This is deliberately not a localization-key sort.
Only this documentation generator and its outputs are owned by this tool.
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "local/campaign"
RAW = ROOT / "local/campaign-audit"
STRINGS_RU = json.loads((DATA / "strings-ru.json").read_text(encoding="utf-8"))
STRINGS_EN = json.loads((DATA / "strings-en.json").read_text(encoding="utf-8"))
RU = {k: v for t in STRINGS_RU.values() for k, v in t.items()}
EN = {k: v for t in STRINGS_EN.values() for k, v in t.items()}
LITERAL='--raw' in sys.argv
if not LITERAL:RU.update(json.loads((ROOT/'localization/ru/campaign.json').read_text(encoding='utf8')))
SPEAKERS = {
    "FI": "Разведка флота", "TS": "Тирра Собан", "KS": "Каран С’Джет",
    "AR": "Амма Радаа", "GR": "Гиитан Радаа", "HA": "Рассказчик",
}

# Node IDs, rather than line keys, retain the link to the actual mission graph.
STAGES = {
    "T1": [
        ("1. Первое подключение Тирры", "После готовности симуляции (`OnSimReady`, узел 764) проходит пять секунд. Тирра впервые ощущает себя частью Материнского корабля. Каран присутствует как наставник.", [259, 567, 405, 409], []),
        ("2. Сенсоры и восприятие", "Событие `IntroFinished` запускает объяснение сенсоров. Продолжение ждёт завершения урока открытия Sensors Manager. Появляется общая цель обучения.", [515, 798, 231, 728, 657, 397], ["MT01_Objective_02"]),
        ("3. Навигация в VR", "После `SensorsFinished` идут перемещение точки обзора, вращение и масштаб, полёт стиком, пошаговый поворот, телепортация и её отмена. Это управление камерой/присутствием игрока, а не новая способность корабля. Последняя ветка вызывает `MovementFinished`.", [137, 306, 135, 585, 161, 278], []),
        ("4. Выделение, движение и первая атака", "После `MovementFinished` появляются учебные корабли. Игрок выбирает ударную группу и проводит её через две зоны (`Detect_SG_Move1`, `Detect_SG_Move2`). После второй зоны создаётся учебный противник и предлагается атака.", [561, 55, 93], []),
        ("5. После уничтожения учебного противника", "`OnWaveDestroyed` для первой учебной группы запускает этот обмен репликами. Противник в этом упражнении не отвечает огнём.", [792, 385, 535, 525], []),
        ("6. Постройка, перегруппировка и списание", "Далее объясняются выбор через палитру команд и тактическая пауза. Игрок строит перехватчик, переносит корабли между группами, списывает корабль и выходит из режима редактирования.", [91, 415, 221, 549, 659], []),
        ("7. Несколько групп и маршрут в обход платформы", "После выхода из редактирования — команды нескольким группам, затем маршрут с контрольными точками. В зоне `Detect_SG_Post_Attack` появляются конечные цели и патрулирующая орудийная платформа. Нужно уничтожить цели, обойдя платформу.", [300, 673, 770], ["MT01_Objective_01"]),
        ("8. Завершение и первый самостоятельный прыжок", "Завершение `MT01_Objective_01` увеличивает счётчик общей цели и снимает учебные задачи. Следуют нижние реплики, общий гиперпрыжок и через восемь секунд `EndMission`.", [437, 360, 663, 467, 171, 439, 545], []),
    ],
    "M1": [
        ("1. Прибытие на полигон и сбор ресурсов", "Основная цепочка начинается от `OnSimReady` (169). Флот приходит раньше Радаа. После диалога выдаётся задача добычи ресурсов.", [28, 479, 80, 597, 26, 563, 499, 46], ["M01_Objective_00"]),
        ("2. Построить разведчик", "Завершение ресурсной цели (`OnObjectiveCompleted`, 321) снимает её, выдаёт следующую и запускает короткое повторение тактической паузы/постройки.", [231, 323], ["M01_Objective_00a"]),
        ("3. Гиитан и поиск первого патруля", "Завершение постройки разведчика (339) запускает появление верфей и разговор с Гиитаном. Первый патруль уже размещается сценарием; игрок должен обнаружить его активным сканированием разведчика.", [299, 401, 52, 447, 647, 523], ["M01_Objective_00b"]),
        ("4. Первый учебный бой", "После выполнения задачи обнаружения (110) выдаётся задача уничтожить первый патруль. Внутреннее имя этого патруля — `patrolC`; буквы тегов не отражают порядок встречи.", [98, 171], ["M01_Objective_01"]),
        ("5. Второй патруль", "Уничтожение `patrolC` (419) создаёт `patrolB`, меняет цель и запускает этот диалог.", [361, 66, 303], ["M01_Objective_01b"]),
        ("6. Третий патруль", "Уничтожение `patrolB` (139) создаёт `patrolA` и следующую цель. Это последний этап совместных учений.", [413, 429], ["M01_Objective_01c"]),
        ("7. Амма предъявляет договор TR-3", "Уничтожение `patrolA` (415) снимает учебную цель. Амма предъявляет претензии, рядом с Материнским кораблём появляются враждебные фрегаты. Разговор идёт в указанном порядке, включая два разных ключа с номером 085. Затем выставляются обе боевые задачи.", [311, 545, 60, 553, 387, 76, 257, 227, 179, 621, 305, 211], ["M01_Objective_02b", "M01_Objective_02"]),
        ("8. Успех: прорыв и отступление", "Выполнение задачи уничтожения ракетных фрегатов (74) снимает обе цели. Скрипт создаёт дополнительные вражеские корабли, даёт разговор об отступлении, запускает общий гиперпрыжок и завершает миссию. Победа здесь — уйти с повреждённым Материнским кораблём.", [385, 507, 613], []),
        ("Условные реплики: повреждение Материнского корабля", "Это отдельные обработчики `33DMG`, `66DMG`, `80DMG`. Они зависят от состояния корабля и не обязаны прозвучать между соседними абзацами основной цепочки. Урон в финале также подталкивается сценарием по таймерам.", [583, 287, 48, 399], []),
        ("Условные реплики: поражение", "Разные ветки потерь. `M01_080_010_GR` относится к раннему исчерпанию сил; `M01_090_010_FI` — к потерям в финальном бою; `M01_100_010_FI` — к слишком тяжёлому повреждению Материнского корабля. Эти реплики не являются продолжением успешного финала.", [143, 263, 153], []),
    ],
    "M4": [
        ("1. Прибытие: погибший хиигарский патруль", "От `OnSimReady` (384) создаются вражеские группы RC1/RC2/RC3 и цель поиска. RC здесь — имена патрульных менеджеров Радаа, а не выдача дружеских сборщиков: каждый содержит два переработчика Радаа и фрегат. Камера показывает выведенные из строя хиигарские корабли. Позже сценарий добавляет другие патрули и сообщает об инженерном корабле; три инженера уже входят в стартовый AdditionalGroups демо-определения.", [277, 23, 342, 217, 336, 75, 61, 394, 332], ["M04_Objective_01"]),
        ("2. Эсминец найден", "Завершение цели поиска (257) ведёт к этому разговору и задаче очистить пространство. Условная проверка перед ним ждёт готовности начального этапа.", [488, 506, 33, 227], ["M04_Objective_02"]),
        ("3. Группа эвакуации Радаа уничтожена", "После выполнения задачи очистки (165) нужно организовать захват/буксировку инженерными кораблями.", [57, 137, 482, 496], ["M04_Objective_03"]),
        ("4. Три инженера закреплены: начинается буксировка", "`OnSquadronCaptured` (508) снимает задачу стыковки, вызывает `destroyerMove`, запускает движение эсминца и защиту. Появление перехватывающих групп дополнительно привязано к зонам маршрута.", [231, 470, 237], ["M04_Objective_04"]),
        ("5. Врата и выбор способа завершения", "Во время буксировки появляются гиперврата, их охрана и новая волна. Выдаётся необязательная задача уничтожения врат. Дальше есть две самостоятельные успешные ветки; это не две обязательные задачи подряд.", [41, 233, 55], ["M04_Objective_05"]),
        ("Финал А. Уничтожить гиперврата", "Завершение `M04_Objective_05` (239) снимает её и задачу защиты, проигрывает эти три реплики, затем запускает общий гиперпрыжок и `EndMission`. Скрипт не требует сначала довести буксир до Материнского корабля.", [450, 225, 376], []),
        ("Финал Б. Довести эсминец к Материнскому кораблю", "Срабатывание зоны `EnemyDetectionSphere` (458) завершает защиту, снимает необязательную цель врат, даёт эту реплику. Затем выполняются два гиперпрыжка: всех союзников и группы с тегом `Capturable`. Взрывать врата для этого финала не требуется.", [388], []),
        ("Условные реплики: состояние Материнского корабля", "Обработчики `99percent` и `50percent`, независимо от основной последовательности.", [29, 49], []),
        ("Условные реплики: поражение", "`YouLose2` / `YouLose3` означают нехватку сил/ресурсов и ведут к первой реплике. `YouLose1` — уничтожение нужного эсминца; `MothershipLost` — потеря Материнского корабля.", [91, 442, 462], []),
    ],
}

EN_NOTES = {
    "M04_010_040_A_TS": "EN: Convenient. It could be a trap. Смысл: «Слишком удобно. Это может быть ловушка».",
    "M04_010_050_A_KS": "EN: When I fought the Taiidani, captured ships were critical for understanding what we were up against. Смысл: Каран вспоминает, что захваченные таииданские корабли помогали понять противника.",
    "M04_010_060_A_TS": "EN: So trap or not, it's a chance worth taking. Смысл: «Ловушка или нет — такой шанс стоит использовать».",
    "M04_010_070_A_KS": "EN: Knowledge is power. Смысл: «Знание — сила».",
    "M04_010_080_A_TS": "EN: Spoken like a true S'jet. Fleet Intelligence, monitor the area for Radaa ships. We are going in. Смысл: Тирра отвечает Каран и приказывает разведке следить за Радаа; флот идёт к эсминцу.",
    "M04_020_030_FI": "EN: All disabled. No signs of life. Здесь говорится о выведенных из строя кораблях без признаков жизни. «Все инвалиды» — ошибка исходного перевода.",
    "M04_Objective_03": "EN: Dock 3 Engineer Craft to the Radaa Destroyer. Нужны ТРИ инженерных корабля, а не «третий».",
    "T01_070_060_TS": "EN: 3... 2... 1... mark. Последнее слово — команда начинать прыжок; «балл» — ошибка перевода.",
}


def quote(key: str, speaker: str | None = None) -> list[str]:
    speaker = speaker or SPEAKERS.get(key.rsplit("_", 1)[-1], "Разведка флота")
    lines = [f"**{speaker}** — `{key}`", ""] + bilingual(key)
    if LITERAL and key in EN_NOTES:
        lines += ["*Примечание к переводу.* " + EN_NOTES[key], ""]
    return lines


def objective(key: str) -> list[str]:
    lines = [f"**Задача** — `{key}`", ""] + bilingual(key)
    if LITERAL and key in EN_NOTES:
        lines += ["*Примечание к переводу.* " + EN_NOTES[key], ""]
    return lines


def bilingual(key: str) -> list[str]:
    lines = []
    for language, label, strings in [("en", "EN — исходный текст", EN), ("ru", "RU — исходная локализация" if LITERAL else "RU — новый перевод", RU)]:
        text = strings.get(key) or ("[Английская строка отсутствует.]" if language == "en" else "[Русская строка отсутствует.]")
        lines += [f"*{label}:*", "", "> " + text.replace("\n", "\n> "), ""]
    return lines


RAW_CACHE: dict[str, dict[int, dict]] = {}
INDEX = json.loads((RAW / "index.json").read_text(encoding="utf-8"))


def raw_file(source: str) -> dict[int, dict]:
    if source not in RAW_CACHE:
        RAW_CACHE[source] = {r["path_id"]: r for r in json.loads((RAW / f"{source}.json").read_text(encoding="utf-8"))}
    return RAW_CACHE[source]


def pointer(source: str, value: dict) -> dict | None:
    if not value.get("m_PathID"):
        return None
    file_id = value.get("m_FileID", 0)
    target = source if not file_id else INDEX["files"][source]["externals"][file_id - 1]
    return raw_file(target).get(value["m_PathID"])


SHIP_DATA = {
    r["data"]["_staticData"]["<Type>k__BackingField"]: {
        "definition": r["name"], "source": r["source"], "path_id": r["path_id"],
        "ru": RU.get(r["data"]["_nameKey"]), "en": EN.get(r["data"]["_nameKey"]),
        "squadron_count": r["data"]["_staticData"]["<SquadronCount>k__BackingField"],
    }
    for r in raw_file("resources.assets").values()
    if r["class_name"] == "Hercules.Designer.ShipDefinition"
}

SHIP_RU_LABELS = {
    1: "Материнский корабль", 9: "Штурмовик Радаа", 10: "Перехватчик",
    11: "Линейный крейсер Радаа", 13: "Ударный бомбардировщик", 14: "Тяжёлый корвет",
    15: "Штурмовой фрегат Радаа", 16: "Носитель", 18: "Штурмовой фрегат",
    19: "Мобильный переработчик", 20: "Ионный фрегат", 21: "Тяжёлый крейсер",
    22: "Фрегат поддержки", 23: "Разведчик", 24: "Многопушечный корвет",
    25: "Мобильный переработчик Радаа", 26: "Инженерный корвет", 27: "Повреждённый эсминец Радаа",
    29: "Лучевой истребитель Радаа", 30: "Эсминец", 31: "Лазерный корвет Радаа",
    32: "Эсминец Радаа", 33: "Командный корвет Радаа", 34: "Тяжёлый ракетный фрегат Радаа",
    35: "Бомбардировщик Радаа", 36: "Гиперврата Радаа", 37: "Корвет Радаа (исходный тип MissileCorvette)",
    38: "Фрегат проникновения Радаа", 39: "Тяжёлая ракетная платформа Радаа", 41: "Верфь Радаа",
    45: "Баррикадный фрегат", 46: "Баллистический эсминец", 50: "Сборщик ресурсов",
}


def ship_label(ship_type: int) -> str:
    data = SHIP_DATA[ship_type]
    return f"{SHIP_RU_LABELS.get(ship_type) or data['ru'] or data['en'] or data['definition']} (`{data['definition']}`)"


def data_members(data: dict) -> collections.Counter:
    if "Type" in data:
        return collections.Counter({data["Type"]: 1})
    counts = collections.Counter(member["Type"] for member in data.get("Members", []))
    if data.get("HasUniqueMember") and data.get("UniqueMemberInit", {}).get("Type"):
        counts[data["UniqueMemberInit"]["Type"]] += 1
    return counts


def count_summary(counts: collections.Counter) -> str:
    if not counts:
        return "Пустая группа: 0 отрядов, 0 корпусов"
    return "; ".join(
        f"{n} отр. / {n * SHIP_DATA[t]['squadron_count']} корп. × {ship_label(t)}"
        for t, n in sorted(counts.items())
    )


def source_label(record: dict) -> str:
    return f"`{record['source']}:{record['path_id']}`"


def spawner_description(record: dict) -> str:
    data = record["data"]
    if record["class_name"].endswith(".PatrolManager"):
        groups = [pointer(record["source"], p) for p in data["_groups"]]
        descriptions = [spawner_description(g) for g in groups if g]
        return "Один из вариантов патруля: " + " / ИЛИ / ".join(descriptions)
    init = data.get("_data", data)
    team = {0: "нейтральная", 1: "игрок", 1024: "Радаа/Computer1", 2048: "Computer2"}.get(init.get("TeamId"), str(init.get("TeamId")))
    tags = ", ".join(init.get("Tags", [])) or "—"
    return f"{team}: {count_summary(data_members(init))}; теги `{tags}`; {source_label(record)}"


def scene_variables(scene: dict) -> dict:
    result = {}
    for container in scene["variables"]:
        entries = container["values"]["declarations"]["collection"]["$content"]
        for entry in entries:
            value = entry["value"]
            if isinstance(value, dict) and value.get("$type") == "UnityEngine.Object":
                result[entry["name"]] = container["object_references"][value["$content"]]
    return result


def spawn_targets(graph: dict, scene: dict, node_id: str) -> list[tuple[str, dict]]:
    nodes = {n["$id"]: n for n in graph["nodes"] if "$id" in n}
    values = collections.defaultdict(list)
    for edge in graph["edges"]:
        if edge["$type"].endswith(".ValueConnection"):
            values[edge["destinationUnit"]["$ref"]].append((edge["destinationKey"], edge["sourceUnit"]["$ref"]))
    variables = scene_variables(scene)
    result = []

    def walk(ident: str, seen: set[str]) -> None:
        if ident in seen:
            return
        seen.add(ident)
        node = nodes[ident]
        if node["$type"].endswith(".GetVariable"):
            name = node.get("defaultValues", {}).get("name", {}).get("$content")
            ref = variables.get(name)
            if ref:
                result.append((name, raw_file(ref["source"])[ref["path_id"]]))
            return
        for _, parent in sorted(values[ident]):
            walk(parent, seen)

    for key, parent in values[node_id]:
        if key in {"EntityInitializer", "AdditionalSpawners"}:
            walk(parent, set())
    assert result, (scene["scene_file"], node_id, "no resolved spawn target")
    return result


def graph_group(graph: dict, node: dict) -> str:
    p = node["position"]
    groups = [n for n in graph["nodes"] if n["$type"].endswith(".GraphGroup") and n["position"]["xMin"] <= p["x"] <= n["position"]["xMax"] and n["position"]["yMin"] <= p["y"] <= n["position"]["yMax"]]
    return ", ".join(n["label"] for n in groups) or "без группы"


def progress_data() -> dict:
    missions = json.loads((DATA / "missions.json").read_text(encoding="utf-8"))
    result = {}
    build_defs = [r for r in raw_file("resources.assets").values() if r["class_name"] == "Hercules.Designer.BuildDefinition"]
    for code, ident, level in [("T1", "Mission_T1_Demo", 1), ("M1", "Mission_M1_Demo", 4), ("M4", "Mission_M4_Demo", 6), ("C1", "Mission_C1", 9)]:
        mission = next(m for m in missions if m["id"] == ident)
        scene = json.loads((DATA / f"level{level}.json").read_text(encoding="utf-8"))
        fleet = []
        for kind in ["default_groups", "additional_groups"]:
            for group in mission[kind]:
                fleet.append({"kind": kind, "name": group["name"], "source": group["source"], "path_id": group["path_id"], "counts": data_members(group["data"])})
        for placement in scene["placements"]:
            if placement["class_name"].endswith((".GroupSpawner", ".SquadronSpawner")) and placement.get("auto_spawn") and placement["data"].get("TeamId") == 1:
                fleet.append({"kind": "scene auto", "name": placement["name"], "source": placement["source"], "path_id": placement["path_id"], "counts": data_members(placement["data"])})
        total = sum((x["counts"] for x in fleet), collections.Counter())
        controller = next(r for r in raw_file(f"level{level}").values() if r["class_name"] == "Hercules.Designer.BuildCommandController")
        commands = controller["data"]["_buildCommandList"]
        refs = [pointer(controller["source"], p) for p in commands["_buildCommands"]]
        mode = "Whitelist" if commands["_controlMode"] == 1 else "Blacklist"
        if mode == "Whitelist":
            allowed = [r for r in refs if not r["data"]["_debugOnly"]]
        else:
            banned = {r["path_id"] for r in refs}
            allowed = [r for r in build_defs if not r["data"]["_debugOnly"] and r["path_id"] not in banned]
        result[code] = {"mission": mission, "scene": scene, "fleet": fleet, "total": total, "controller": controller, "mode": mode, "listed": refs, "allowed": allowed}
    assert [len(result[m]["allowed"]) for m in ["T1", "M1", "M4", "C1"]] == [1, 4, 6, 13]
    assert sum(result["M1"]["total"].values()) == 9
    assert sum(n * SHIP_DATA[t]["squadron_count"] for t, n in result["M1"]["total"].items()) == 37
    assert sum(result["M4"]["total"].values()) == 15
    assert sum(n * SHIP_DATA[t]["squadron_count"] for t, n in result["M4"]["total"].items()) == 45
    return result


def compact_progress(code: str, data: dict) -> list[str]:
    p = data[code]
    total = p["total"]
    lines = ["### Флот и постройка: кратко", "", f"Старт: **{p['mission']['starting_ru']} RU**; {sum(total.values())} отрядов/самостоятельных крупных единиц, **{sum(n * SHIP_DATA[t]['squadron_count'] for t, n in total.items())} физических корпусов** до действий игрока. Перенос флота в демо-определении отключён.", "", count_summary(total) + ".", "", "Доступные команды строительства: " + "; ".join(f"`{r['name']}`" for r in p["allowed"]) + ".", ""]
    notes = {
        "T1": "На старте только Материнский корабль; два учебных подкрепления добавят по три отряда перехватчиков (по 15 корпусов). При уроке тактической паузы узел 782 выдаёт ещё 1000 RU. Строительство ограничено перехватчиком, а доступ к интерфейсу открывается по урокам.",
        "M1": "Все четыре строительные команды разрешены контроллером уже при загрузке. Постройка разведчика — задача, а не исследование, открывающее новый класс. Последовательно появляются три учебных патруля, три фрегата в сцене предательства, гиперврата с подкреплениями и силы, от которых требуется уйти прыжком.",
        "M4": "Три инженера из `AdditionalGroups` — уже стартовое подкрепление, их не нужно ждать до реплики `FI_UnlockEngineerCraft`. Все шесть строительных команд разрешены при загрузке; отдельного исследовательского переключателя после этой реплики в графе нет. RC1/RC2/RC3 — вражеские патрули, не дружеские сборщики. Захватываемый повреждённый эсминец размещён в сцене отдельно.",
        "C1": "Шесть `DefaultGroups` пусты: предписанного боевого флота нет. Начальный доступный флот игрок формирует сам. Контроллер использует BLACKLIST: носитель и debug-переработчик запрещены, остальные 13 недебажных типов доступны. Это не список из двух доступных кораблей.",
    }
    lines += [notes[code], "", "Точные группы, составы, узлы появления, цены и основания доступности — в [DEMO_PROGRESSION.md](DEMO_PROGRESSION.md).", ""]
    return lines


def write_progression(data: dict) -> None:
    lines = """# Steam-демка: флот, постройка и сюжетные открытия

Этот документ относится **только к установленной Steam-демке**, проверенной по извлечённым данным 17 октября 2026 года. Он не описывает полную Quest-версию и не изменяет мод. Читаемые реплики и задачи на EN/RU — в [DEMO_SCENARIOS.md](DEMO_SCENARIOS.md).

## Важное различие: слот, отряд, физический корабль

Одна запись `GroupInitialization.Members` — **один отряд типа ShipType**, а не обязательно один физический корпус. `State.SpawnGroup` создаёт отряд для каждой записи; `State.SpawnSquadron` создаёт внутри него `ShipStaticData.SquadronCount` кораблей. Поэтому перенос «одна запись Members = один HWRM-корабль» уменьшает исходный флот.

Источники: `local/decompiled-demo/Hercules.Simulation/State.cs`, методы `SpawnSquadron` (около строки 1714, цикл на 1723) и `SpawnGroup` (около 1987); `local/campaign-audit/resources.assets.json`, соответствующий `Hercules.Designer.ShipDefinition`, `_staticData.<SquadronCount>k__BackingField`. Группа Strike Group может содержать несколько таких отрядов.

Начальный флот ниже — предписанный определением миссии плюс автоматические дружеские размещения сцены, **до свободной постройки игроком**. `LoadoutSpawner.BuildLoadout` добавляет `AdditionalGroups` сразу после DefaultGroups/перенесённых групп, а не после сюжетной реплики. У всех четырёх рассматриваемых определений `AllowCarryover=false`.

| Эпизод | RU | Отрядов/крупных единиц на старте | Физических корпусов | Разрешённых строительных типов |
|---|---:|---:|---:|---:|
""".splitlines()
    for code, p in data.items():
        total = p["total"]
        lines.append(f"| {code} | {p['mission']['starting_ru']} | {sum(total.values())} | {sum(n * SHIP_DATA[t]['squadron_count'] for t, n in total.items())} | {len(p['allowed'])} |")
    lines += ["", "В C1 шесть DefaultGroups пусты; отряды игрока для боя не заданы жёстко. В T1 учебные группы выдаются позже. В M4 нейтральный повреждённый эсминец не посчитан частью стартового флота игрока.", "", "### Размеры отрядов, влияющие на числа", "", "| Тип | Корпусов в отряде | Точный источник |", "|---|---:|---|"]
    relevant = sorted({t for p in data.values() for t in p["total"]} | {9, 35, 29, 31, 24, 37})
    for t in relevant:
        s = SHIP_DATA[t]
        lines.append(f"| {ship_label(t)} | {s['squadron_count']} | `{s['source']}:{s['path_id']}` |")
    lines += ["", "## Как включается строительство", "", "`BuildCommandController.Awake` применяет список сразу при загрузке сцены. В `BuildCommandList` режим **1 = Whitelist** разрешает только перечисленные команды, **0 = Blacklist** разрешает все недебажные команды, кроме перечисленных. `BuildCommandDatabase.SetUnlockModeAll` всегда блокирует `DebugOnly`; `BuildDefinition.IsUnlocked` читает этот флаг доступности. Это разрешение постройки, а не оплачиваемое исследование технологии.", "", "В доступных графах T1/M1/M4 нет подключённого `SetBuildByBuildList` и нет цепочки покупки/завершения исследований. Их общий подграф `GeneralAchievements` — достижения. Сам класс `SetBuildByBuildList.cs` существует в коде, однако наличие класса ещё не доказывает его использование конкретной картой.", "", "Цены ниже — за **отряд/slot**, не за один физический корпус. Время — `_duration` во время боя; `BuildDefinition.Duration` возвращает 1 секунду в Planning Phase. Множитель сложности/изменение времени симуляции здесь не пересчитывается.", ""]
    for code, p in data.items():
        m = p["mission"]
        lines += [f"## {code}: старт и разрешённая постройка", "", f"Определение `{m['id']}` — `{m['source']}:{m['path_id']}`; карта `{p['scene']['scene_file']}`; RU={m['starting_ru']}, FleetCap={m['fleet_cap']}, Carryover={m['carryover']}.", "", "| Источник старта | Группа | Состав | Ссылка |", "|---|---|---|---|"]
        for entry in p["fleet"]:
            lines.append(f"| {entry['kind']} | `{entry['name']}` | {count_summary(entry['counts'])} | `{entry['source']}:{entry['path_id']}` |")
        controller = p["controller"]
        lines += ["", f"Контроллер {source_label(controller)}, режим **{p['mode']}**. Явно перечислено: " + ", ".join(f"`{r['name']}`" for r in p["listed"]) + ".", "", "| Разрешено построить | Отряд/корпусов | RU | Секунд в бою | BuildDefinition |", "|---|---:|---:|---:|---|"]
        for build in p["allowed"]:
            d = build["data"]
            lines.append(f"| {ship_label(d['_shipType'])} | 1/{SHIP_DATA[d['_shipType']]['squadron_count']} | {d['_cost']} | {d['_duration']:g} | `{build['name']}`, {source_label(build)} |")
        lines += [""]
        if code == "C1":
            lines += ["**Это BLACKLIST.** `Build_Kus_Carrier` и `Build_Kus_MobileRefinery` не предлагаются к обычной постройке. Остальные 13 недебажных типов открыты с начала сцены; по мере волн отдельные новые типы контроллер не исследует и не открывает.", ""]
        elif code == "M4":
            lines += ["**Три инженера уже входят в старт:** `Group_M4_Default_4` в AdditionalGroups. `FI_UnlockEngineerCraft` (узел 332) произносится после стартового разговора и патрульных появлений, но сам по себе не включает команду постройки: `Build_Kus_EngineerCorvette` разрешён контроллером при загрузке. Аналогично тяжёлый корвет доступен уже при загрузке M4; его отдельная строка открытия в этих трёх графах не подключена.", "", "На карте также автоматически размещён **нейтральный повреждённый эсминец**, `level6:1930`, теги `DamagedDestroyer`, `Capturable`. После сцепления инженеров граф меняет его команду на Computer2, а не добавляет обычный свободно управляемый эсминец в стартовый флот игрока: узел 65 `SetEntityTeamId`.", ""]
        elif code == "T1":
            lines += ["Уроки последовательно открывают управление интерфейсом. Это не новые исследованные корпуса: единственная разрешённая команда постройки весь эпизод — перехватчик. При тактической паузе после ожидания узла 575 срабатывает `AddRU`, узел **782: +1000 RU Player1**.", ""]
        else:
            lines += ["Добыча до общей суммы 200 RU и постройка разведчика — последовательные цели `M01_Objective_00`, `_00a`. Сканирование — `_00b`. Контроллер уже разрешил постройку всех четырёх типов; достижение 200 RU не завершает отдельное исследование и не добавляет новый BuildDefinition.", ""]
        if code in {"T1", "M1", "M4"}:
            graph = json.loads((DATA / f"Mission_{code}-graph.json").read_text(encoding="utf-8"))
            lines += ["### Что добавляет сценарий", "", "Таблица перечисляет подключённые SpawnEntity и их реальные цели. Числа — отряды и физические корпуса **за одно срабатывание**. PatrolManager выбирает один вариант и свободный маршрут; повторные таймеры могут давать дополнительные срабатывания. Порядок узлов в таблице по ID служит ссылкой, хронология — в читаемом сценарии.", "", "| Узел графа / группа редактора | Переменная сцены | Что создаётся |", "|---|---|---|"]
            for node in graph["nodes"]:
                if node["$type"].endswith(".SpawnEntity"):
                    for alias, target in spawn_targets(graph, p["scene"], node["$id"]):
                        lines.append(f"| `Mission_{code}`:{node['$id']} — {graph_group(graph, node)} | `{alias}` → {source_label(target)} | {spawner_description(target)} |")
            lines += [""]
    lines += ["## Условия появления, которые легко перепутать", "", "- **T1:** 163 создаёт StrikeGroupA, 187 — StrikeGroupB: каждая содержит 3 отряда перехватчиков, то есть 15 корпусов. Уничтожаемые учебные цели — реальные Radaa-типы в симуляции, но с учебными ограничениями/неуязвимостью; это не новый союзный флот.", "- **M1:** после постройки разведчика узел 219 создаёт один отряд штурмовиков Радаа (5 корпусов), а узел 359 — нейтральную верфь Радаа. Затем последовательно идут patrolC → patrolB → patrolA. Предательство создаёт по одному ракетному/инфильтрационному фрегату узлами 555/120/631.", "- **M1:** `CreateHealthEvent` 273 следит за тегом `capture` на пороге 99% и вызывает `spawnHSG`. Этот обработчик создаёт врата (611) и патруль D (267). Патруль E повторяется узлом 199/таймером 557 через 60 секунд; уничтожение группы с тегом `Carrier` останавливает таймер. Гиперврата имеют именно этот неожиданный тег.", "- **M1:** финальная группа 607 создаёт ещё четыре отдельных missile-frigate spawner и EndShips. Это угроза для постановочного отхода, а не обязательные новые цели на уничтожение.", "- **M4:** RC1/RC2/RC3 в узле 422 — три вражеских патруля; каждый содержит два переработчика Радаа и один фрегат. Это **6 вражеских переработчиков + 3 фрегата**, не выдача ресурсных кораблей игроку. Два своих сборщика уже содержатся в стартовом Group_M4_Default_3.", "- **M4:** после сцепления трёх инженеров (OnSquadronCaptured 508) начинается буксировка. Гиперврата и охрана появляются узлами 25/67; финальная волна — 366. Патрули 21/494 также зависят от зон маршрута и повторной логики. Узел AddRU 474 содержит **0 RU**, денежной наградой его считать нельзя.", "", "## C1: пул противников и волны", "", "`level9:486`, ChallengeModeController: 20 WaveDefinition; 42 секунды до первой волны, 50 секунд между появлениями, отсчёт последующих волн — за 10 секунд. До уничтожения предыдущей волны контроллер не ждёт. В таблице — допустимые типы/составы групп, **не фиксированное количество врагов волны**. Количество повторений групп выбирается по бюджету мощности; одинаковые типы могут набираться несколько раз.", "", "| Волна | WaveDefinition | Допустимые группы для набора |", "|---:|---|---|"]
    c1 = data["C1"]
    controller = next(r for r in raw_file("level9").values() if r["class_name"] == "Hercules.Designer.ChallengeModeController")
    for i, ref in enumerate(controller["data"]["_waveDefinitions"], 1):
        wave = pointer("level9", ref)
        descriptions = [spawner_description(pointer(wave["source"], group)) for group in wave["data"]["AvailableGroups"]]
        lines.append(f"| {i} | `{wave['name']}`, {source_label(wave)} | " + " / ИЛИ / ".join(descriptions) + " |")
    lines += ["", "## Реплики об открытиях: что подключено, а что только лежит в таблицах", "", "**Оплачиваемого дерева исследований в этих четырёх сценах не найдено.** В трёх миссионных графах корпуса доступны через списки сцены, задачи и интерфейсные ограничения. C1 с начала разрешает почти весь недебажный набор. Слова «technology», «engineering» и «can now build» в диалоге не означают автоматического существования отдельного исследования.", "", "Ниже сохранены буквальные EN и RU. Из перечисленных объявлений в доступных трёх графах реально подключено только `FI_UnlockEngineerCraft`. Остальные строки присутствуют в Steam-демке как материал дальнейшей кампании; их карты/условия открытия по одним этим строкам не восстановлены.", ""]
    graphs = {m: json.loads((DATA / f"Mission_{m}-graph.json").read_text(encoding="utf-8")) for m in ["T1", "M1", "M4"]}
    connected = collections.defaultdict(list)
    for m, graph in graphs.items():
        for node in graph["nodes"]:
            if node["$type"].endswith(".PlayDialogue"):
                connected[node["resolved_objects"]["_dialogueLine"]["text_key"]].append(f"Mission_{m}:{node['$id']}")
    for key in ["FI_UnlockHeavyCorvette", "FI_UnlockEngineerCraft", "FI_UnlockMultiGunCorvette", "FI_UnlockAssaultFrigate", "FI_UnlockBarricadeFrigate", "FI_UnlockIonFrigate", "FI_UnlockDestroyer", "FI_UnlockBalisticDestroyer", "FI_UnlockHeavyCruiser"]:
        status = ", ".join(connected[key]) if connected[key] else "Только строка в таблице; нет вызова в T1/M1/M4"
        lines += [f"### `{key}`", "", f"Статус: **{status}**. Источник текста: `Strings_Missions`, ключ `{key}`.", ""] + quote(key, "Разведка флота")
    lines += ["### Другие связанные реплики в доступных миссиях", "", "Это сюжет/инструкции о ресурсах, строительстве и технологиях, а не дополнительные найденные исследования.", ""]
    for key in ["T01_050_010_FI", "M01_025_010_FI", "M01_025_020_FI", "M01_050_020_KS", "M01_060_030_AR", "M04_040_040_FI"]:
        lines += ["Подключение: " + ", ".join(f"`{p}`" for p in connected[key]) + ".", ""] + quote(key)
    lines += ["## Что не следует принимать за реальное подкрепление", "", "В сценах есть шаблоны GroupSpawner/SquadronSpawner, у которых `_autoSpawn=0` и нет подключённого появления в найденных графах. Например, `level4:433` — большая дружеская тестовая ClusterInterceptors-группа; `level4:439` — отдельный сборщик. Они не добавлены в стартовый флот и не посчитаны подкреплениями только потому, что записи существуют в сцене. Аналогично текст нового корабля в Strings_Missions не добавляет его автоматически в строительство.", "", "## Источники и границы", "", "- `local/campaign/missions.json`: Mission_T1_Demo/M1_Demo/M4_Demo и Mission_C1; стартовые RU, DefaultGroups, AdditionalGroups, Carryover и FleetCap.", "- `local/campaign/level1.json`, `level4.json`, `level6.json`, `level9.json`: сохранённые группы, сцены, переменные и размещения.", "- `local/campaign-audit/level*.json` и `resources.assets.json`: исходные BuildCommandController, BuildDefinition, ShipDefinition и PatrolManager; точные source:path_id приведены рядом с записями.", "- `local/campaign/Mission_{T1,M1,M4}-graph.json`: ID конкретных управляющих узлов появления и реплик.", "- `local/decompiled-demo/Hercules/LoadoutSpawner.cs`: DefaultGroups/AdditionalGroups и назначение RU.", "- `local/decompiled-demo/Hercules.Designer/{BuildCommandController,BuildCommandList,BuildCommandDatabase,BuildDefinition}.cs`: whitelist/blacklist, debug-флаги, цена и время.", "- `local/decompiled-demo/Hercules.Designer.Mission/PatrolManager.cs` и `SpawnEntity.cs`: выбор состава/маршрута и запуск спавнеров.", "- `local/decompiled-demo/Hercules.Designer/ChallengeModeController.cs`: волны и победа C1.", "", "Это статический разбор извлечённых данных и декомпиляции, без запуска игры. Он фиксирует правила сцены, а не измеренное конкретное прохождение. Привязка строк дальнейших эпизодов к отсутствующим картам здесь не выдумывается; полная Quest-версия должна рассматриваться отдельным источником.", ""]
    (ROOT / "docs/DEMO_PROGRESSION.md").write_text("\n".join(lines), encoding="utf-8")


def timeline_dialogues(filename: str) -> list[dict]:
    records = json.loads((RAW / filename).read_text(encoding="utf-8"))
    by_id = {r["path_id"]: r for r in records}
    clips = []
    for record in records:
        for clip in record["data"].get("m_Clips", []):
            asset = by_id.get(clip.get("m_Asset", {}).get("m_PathID"))
            if not asset or asset["class_name"] != "Hercules.DialogueAudioAsset":
                continue
            line = by_id[asset["data"]["Data"]["DialogueLine"]["m_PathID"]]
            clips.append({"time": clip["m_Start"], "key": line["data"]["_textKey"]})
    clips.sort(key=lambda x: x["time"])
    assert len(clips) == 8, (filename, clips)
    return clips


def main() -> None:
    progression = progress_data()
    content = """# Что есть в демке: сценарии для чтения

Сверено по установленной Steam-демке 17 октября 2026 года. Здесь три эпизода основного демо-маршрута: **T1 → M1 → M4**, два вступительных аниматика и отдельный бонус **C1**. Это чтение исходного материала, а не отчёт о прохождении нового мода.

В данных есть определения **11 миссий полной кампании** и тексты дальнейшего сюжета. Это не означает, что в демке есть 11 игровых карт: содержательно присутствуют карты T1 (`level1`), M1 (`level4`), M4 (`level6`) и C1 (`level9`), плюс сцены освещения и два вступления. Промежуточные миссии между M1 и M4 в демке отсутствуют. Стык этих эпизодов нужно делать явно, не выдавая его за полный оригинальный маршрут.

## Как читать

У каждой реплики и задачи отдельно приведены **буквальный EN** и **буквальный RU из исходной локализации**. Перевод местами ошибочный: «разрушитель» означает эсминец, «поезд с Радаа» — учения с Радаа; род говорящих иногда неверен. В наиболее существенных местах добавлено пояснение. Отсутствующий русский текст явно отмечен и не подменён сочинённой «оригинальной» репликой. Данные флота и строительства кратко приведены у каждой миссии, подробная сверка — в [DEMO_PROGRESSION.md](DEMO_PROGRESSION.md).

Порядок основных сцен восстановлен по **управляющим рёбрам Unity Visual Scripting**, событиям завершения задач и тегам волн. Реплики аниматиков расположены по времени клипов **Timeline**. Порядок строк в таблице локализации не использовался как доказательство порядка игры. Развилки, сообщения о повреждении и поражения вынесены отдельно: они зависят от действий игрока и могут прерывать основную цепочку. Тайминги динамической сцены и видимость каждого объекта здесь не проверялись запуском игры.

Технические ключи рядом с репликами позволяют найти исходник. **FI** — Разведка флота, **TS** — Тирра Собан, **KS** — Каран С’Джет, **AR** — Амма, **GR** — Гиитан. Вступление M1 обозначено в исходнике как реплики рассказчика, хотя ключи заканчиваются на HA.

## Кратко о сюжете доступного фрагмента

После возвращения на Хиигару и войны со Тварью хиигаряне сотрудничают с торговцами Радаа. Тирра Собан принимает управление старым Материнским кораблём; Каран обучает её прямой связи с кораблём. Совместные учения оборачиваются попыткой Радаа силой получить гиперпространственное ядро, ссылаясь на старый договор с императором Таиидана. Флот уходит с повреждениями. Позже приходит чужой сигнал бедствия: можно захватить эсминец Радаа, чтобы изучить противника. На месте обнаруживаются бесследно выведенные из строя хиигарские корабли — намёк на неизвестное оружие. Захват эсминца завершает доступный сюжетный фрагмент, но не всю историю.

## Вступление M1: сохранить отдельно от VR-обучения

`M1_Animatic_Intro`, игровая сцена `level3`, данные Timeline в `sharedassets3.assets`. В демо-цепочке это вступление назначено определению **Mission_T1_Demo**, а не **Mission_M1_Demo**: удаление T1 целиком без переноса вступления потеряет экспозицию.

Это самостоятельный сюжетный пролог: Хиигара после изгнания, война со Тварью, приход Радаа, восстановление Материнского корабля, уход Каран в наставники и назначение Тирры. Для HWRM его можно показывать перед первой боевой миссией, даже если упражнения с VR-контроллерами убрать.
""".splitlines()
    content += [""]
    intro1 = timeline_dialogues("sharedassets3.assets.json")
    for clip in intro1:
        content += [f"*Начало клипа: {clip['time']:.2f} с.*", ""] + quote(clip["key"], "Рассказчик")

    mission_order = {}
    for mission, title, preamble in [
        ("T1", "T1. Подключение и основные приёмы управления", "`T1_CoreControls`, `level1`, граф `Mission_T1`. В определении демо: 5000 RU, лимит флота 30, перенос флота отключён. Это полноценная сцена знакомства Тирры с кораблём, совмещённая с VR-инструктажем."),
        ("M1", "M1. Испытательный полигон Хиигара", "`M1_Hiigara Proving Grounds`, `level4`, граф `Mission_M1`. Демо-определение: 100 RU, лимит 30, перенос флота отключён. Начальная заявка `Train with the Radaa` означает совместные учения. Исходное русское «Поезд с Радаа» — ошибка."),
        ("M4", "M4. Потерянный эсминец", "`M4_AKeyAsset`, `level6`, граф `Mission_M4`. Демо-определение: 1200 RU, лимит 33, перенос флота отключён. Название в локализации — `The Lost Destroyer`, рабочее имя сцены — `A Key Asset`. Задача — получить корабль противника для анализа, а не просто уничтожить его."),
    ]:
        content += [f"## {title}", "", preamble, ""]
        content += compact_progress(mission, progression)
        if mission == "M4":
            content += ["### Вступительный аниматик M4", "", "`M4_Animatic_Intro`, `level8`, Timeline в `sharedassets8.assets`. **Русские строки 040–080 не соответствуют английскому диалогу**: они сдвинуты или повторяют предыдущие фразы. Для переноса нужно исправить текст; ниже ошибка сохранена для сверки.", ""]
            for clip in timeline_dialogues("sharedassets8.assets.json"):
                content += [f"*Начало клипа: {clip['time']:.2f} с.*", ""] + quote(clip["key"])
        graph = json.loads((DATA / f"Mission_{mission}-graph.json").read_text(encoding="utf-8"))
        nodes = {int(n["$id"]): n for n in graph["nodes"] if "$id" in n}
        expected = collections.Counter(next(iter(n["resolved_objects"].values()))["text_key"] for n in nodes.values() if n["$type"].endswith(".PlayDialogue"))
        used = []
        mission_order[mission] = []
        for heading, context, ids, tasks in STAGES[mission]:
            content += [f"### {heading}", "", context, ""]
            keys = []
            for node_id in ids:
                node = nodes[node_id]
                assert node["$type"].endswith(".PlayDialogue"), (mission, node_id)
                key = node["resolved_objects"]["_dialogueLine"]["text_key"]
                keys.append(key)
                used.append(key)
                content += quote(key)
            for task in tasks:
                content += objective(task)
            mission_order[mission].append({"heading": heading, "context": context, "node_ids": ids, "dialogue_keys": keys, "objective_keys": tasks})
        assert set(used) == set(expected), (mission, set(expected) - set(used), set(used) - set(expected))
        assert len(used) == len(set(used)), (mission, "duplicate reading entries")
        if mission == "T1":
            content += ["### Что делать с обучением в HWRM", "", "Полный VR-инструктаж переносить не требуется: жесты, вращение мира руками, телепортация точки обзора, палитра на запястье и перекладывание кораблей в режиме редактирования привязаны к VR. В HWRM это заменяется обычными камерой, выделением, приказами, строительством и паузой.", "", "**Сюжетную рамку стоит оставить.** Особенно: первое подключение Тирры (`T01_010_*`), ограничения восприятия и наставления Каран (`T01_030_040_TS`, `T01_030_050_KS`), ощущение кораблей частью себя и предупреждение о потерях (`T01_040_060_KS`–`T01_040_080_KS`, `T01_050_040_KS`–`T01_050_060_KS`), самостоятельный прыжок к Радаа (`T01_070_*`). Это знакомство двух командующих, а не только справка по кнопкам.", "", "Можно сократить T1 до короткого пролога/системного теста и сразу переходить к M1. Вступительный аниматик M1 при этом обязателен для понятной экспозиции. Исходный граф имеет 39 узлов PlayDialogue, но 38 разных ключей: `T01_030_013_FI` дублируется в узле 145 без входящего управляющего ребра. Здесь эта реплика напечатана один раз в основной ветке. Ещё несколько незадействованных навигационных заготовок графа не превращены в обязательные упражнения.", ""]

    content += challenge_section(progression)
    total = sum(len({k for s in ss for k in s["dialogue_keys"]}) for ss in mission_order.values())
    content += ["## Для решения о переносе", "", "**Обучение можно пропустить как игровой VR-урок, но лучше сохранить его сюжетный каркас.** Убираются длинные упражнения с руками и телепортацией камеры. Остаются вводный аниматик, краткая сцена первого подключения Тирры, несколько реплик Каран и первый прыжок. M1 и M4 уже дают основу небольшой сюжетной кампании: учения → предательство → эвакуация → поиск и захват эсминца. Между M1 и M4 потребуется честно обозначенный переход, поскольку промежуточная карта в демке отсутствует. C1 удобно оставить отдельной тренировкой/бонусом: для понимания фабулы он не нужен.", "", "## Сверка и пределы восстановления", "", f"В чтение включены **{total} разных реплик из трёх миссионных графов** (T1 — 38, M1 — 45, M4 — 32) и **16 реплик двух вступительных Timeline**. Это 131 различная реплика сюжетного/учебного фрагмента, включая условные поражения и сообщения. Дополнительно выписаны общие задачи и экранные сообщения C1. Из 116 узлов PlayDialogue только одна повторная T1-реплика не продублирована в чтении.", "", "Источники в рабочем проекте:", "", "- `local/campaign/Mission_T1-graph.json`, `Mission_M1-graph.json`, `Mission_M4-graph.json`: реальные узлы и управляющие/значимые связи.", "- `local/campaign/strings-ru.json`, `strings-en.json`, `transcript-missions.json`, `transcript-animatics.json`: буквальные строки и привязка к звуку.", "- `local/campaign/missions.json`, `level1.json`, `level4.json`, `level6.json`, `level9.json`: маршрут, стартовые параметры, размещения и области.", "- `local/campaign-audit/sharedassets3.assets.json`, `sharedassets8.assets.json`: порядок реплик по времени клипов аниматиков.", "- `local/campaign-audit/level9.json`, `sharedassets9.assets.json`, `local/decompiled-demo/Hercules.Designer/ChallengeModeController.cs`: параметры и поведение C1.", "- `local/campaign/scenario-order.json`: порядок разделов и исходные ID узлов для последующей сверки скриптов.", "", "Наличие текста/озвучки дальнейших миссий не принято за наличие их карт. Изображения аниматиков, постановка камер, точное звучание всех веток и сохранение темпа в HWRM требуют отдельной проверки. Реплики здесь восстановлены из данных; неизвестные события отсутствующих уровней не досочинены.", ""]
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    if not LITERAL:
        content=[line.replace('У каждой реплики и задачи отдельно приведены **буквальный EN** и **буквальный RU из исходной локализации**. Перевод местами ошибочный: «разрушитель» означает эсминец, «поезд с Радаа» — учения с Радаа; род говорящих иногда неверен. В наиболее существенных местах добавлено пояснение. Отсутствующий русский текст явно отмечен и не подменён сочинённой «оригинальной» репликой.', 'Реплики кампании и обучения заново переведены с английского с учётом сюжета и говорящих. EN сохранён для сверки. Буквальная старая локализация — в [DEMO_SCENARIOS_RAW.md](DEMO_SCENARIOS_RAW.md). Бонус C1 пока дан в исходной локализации и не включён в экспорт кампании.').replace('**Русские строки 040–080 не соответствуют английскому диалогу**: они сдвинуты или повторяют предыдущие фразы. Для переноса нужно исправить текст; ниже ошибка сохранена для сверки.', 'Русский текст исправлен по английскому диалогу; сдвинутые и повторные строки исходного перевода сохранены в RAW-версии.') for line in content]
    output = docs / ("DEMO_SCENARIOS_RAW.md" if LITERAL else "DEMO_SCENARIOS.md")
    output.write_text("\n".join(content), encoding="utf-8")
    if not LITERAL:write_progression(progression)
    (DATA / "scenario-order.json").write_text(json.dumps({"method": "authored chapters from control edges, objective/event transitions; intro clips by Timeline start", "missions": mission_order, "intros": {"M1": intro1, "M4": timeline_dialogues("sharedassets8.assets.json")}}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(output), "progression": str(docs / "DEMO_PROGRESSION.md"), "mission_dialogue_unique": total, "intro_dialogue_unique": 16, "chapters": {m: len(v) for m, v in mission_order.items()}, "allowed_build_types": {m: len(v['allowed']) for m, v in progression.items()}}, ensure_ascii=False))


def challenge_section(progression: dict) -> list[str]:
    lines = ["## C1. Отдельный бонус: защита от волн", "", "**C1 не входит в основной `_demoMissions`-маршрут T1 → M1 → M4.** Это определение `Mission_C1` из `_challengeMissions`; сама карта `level9` содержательно присутствует. Доступ через меню конкретной демо-сборки здесь запуском не проверялся. Для переноса можно подключать отдельно, без превращения в очередную сюжетную главу.", "", "В этой сцене нет отдельного найденного миссионного графа диалогов. Режим ведёт `ChallengeModeController`: защита Материнского корабля, последовательные волны Радаа, очки и итоговый ранг. Это боевое испытание, а не новая глава истории Тирры.", "", "### Ход испытания", "", "По определению миссии — 5000 стартовых RU и лимит 40. Через три секунды контроллер выдаёт две задачи. Первая волна назначена на 42-ю секунду времени симуляции; следующие идут через 50 секунд от фактического появления предыдущей. Ожидание уничтожения предыдущей волны в таймере не требуется, поэтому противники могут накапливаться. Для последующих волн обратный отсчёт начинается за десять секунд до появления; для первой волны отдельного десятисекундного старта контроллер не задаёт. Всего настроено **20 волн**.", ""]
    lines += compact_progress("C1", progression)
    for key in ["C_Objective_01", "C_Objective_02"]:
        lines += objective(key)
    for key in ["C_FirstWavePrompt", "C_WaveSpawned"]:
        lines += quote(key)
    lines += ["Начальный доклад выбирается случайно из набора, доклады о волнах — из наборов первой/ранних/поздних/последней волны. Это ситуативные сообщения Разведки флота, не разговоры героев в фиксированном порядке. В таблице строк присутствуют, например, такие варианты; отсутствие отдельной привязки каждого набора в извлечённой сцене не позволяет выдавать весь список локализации за точную дорожку одного прохождения:", ""]
    for key in ["FI_ChallengeMode_Objective_02", "FI_ChallengeMode_Objective_03", "M04_060_010_FI_CM", "M07_010_140_A_FI_CM", "M07_020_020_FI_CM"]:
        lines += quote(key)
    lines += ["### Состав волн", "", "Таблица показывает настройки генератора, а не точный неизменный флот. Контроллер набирает группы из допустимого списка до заданной мощности, учитывая максимальный бюджет; точки появления выбираются из разрешённых классов дальности. В `GuaranteedGroups` у всех этих волн пусто.", "", "| Волна | Бюджет мощности, min–max | Класс точки появления |", "|---:|---:|---|"]
    raw = json.loads((RAW / "sharedassets9.assets.json").read_text(encoding="utf-8"))
    waves = [r for r in raw if r["class_name"] == "Hercules.Designer.WaveDefinition"]
    waves.sort(key=lambda r: int(r["name"].removeprefix("Wave_Test")))
    assert len(waves) == 20
    for record in waves:
        d = record["data"]
        lines.append(f"| {record['name'].removeprefix('Wave_Test')} | {d['MininumPower']:g}–{d['MaximumPower']:g} | {', '.join(d['AllowedSpawnPointTags'])} |")
    lines += ["", "### Завершение", "", "Успех наступает после уничтожения всех 20 волн. Отдельные поражения — потеря Материнского корабля, исчерпание оборонительных возможностей/ресурсов либо выход игрока. Итоговые тексты ниже; не все они звучат в одном прохождении.", ""]
    for key in ["C_ChallengeComplete_FI", "C_ChallengeFailed_Mothership_FI", "C_ChallengeFailed_Resources_FI", "C_ChallengeFailed_Forfeit"]:
        lines += quote(key)
    lines += ["Нового сюжетного решения в C1 не найдено. Для мини-кампании его можно опустить, а затем использовать как отдельный тест экономики и баланса.", ""]
    return lines


if __name__ == "__main__":
    main()
