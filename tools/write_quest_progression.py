"""Read already extracted Quest data; write only QUEST_PROGRESSION.md.

No Unity audit, decompilation, game execution, or Steam output modification.
"""
from __future__ import annotations

import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "local/quest-campaign"
RAW = ROOT / "local/quest-audit"
INDEX = json.loads((RAW / "index.json").read_text(encoding="utf-8"))
MISSIONS = json.loads((DATA / "missions.json").read_text(encoding="utf-8"))
STRINGS = {
    lang: {k: v for table in json.loads((DATA / f"strings-{lang}.json").read_text(encoding="utf-8")).values() for k, v in table.items()}
    for lang in ["en", "ru"]
}
STRINGS['ru'].update(json.loads((ROOT/'localization/ru/campaign.json').read_text(encoding='utf8')))
CACHE: dict[str, dict[int, dict]] = {}


def raw_file(source: str) -> dict[int, dict]:
    if source not in CACHE:
        CACHE[source] = {r["path_id"]: r for r in json.loads((RAW / f"{source}.json").read_text(encoding="utf-8"))}
    return CACHE[source]


def pointer(source: str, value: dict) -> dict | None:
    if not value.get("m_PathID"):
        return None
    file_id = value.get("m_FileID", 0)
    target = source if not file_id else INDEX["files"][source]["externals"][file_id - 1]
    return raw_file(target).get(value["m_PathID"])


def records_of_type(class_name: str) -> list[dict]:
    sources = {r["source"] for r in INDEX["mono_types"] if r["class_name"] == class_name}
    return [r for source in sorted(sources) for r in raw_file(source).values() if r["class_name"] == class_name]


SHIP_RECORDS = records_of_type("Hercules.Designer.ShipDefinition")
SHIPS = {r["data"]["_staticData"]["<Type>k__BackingField"]: r for r in SHIP_RECORDS}
BUILDS = records_of_type("Hercules.Designer.BuildDefinition")
DATABASE = records_of_type("Hercules.Designer.MissionDatabase")[0]
assert len(SHIP_RECORDS) == 46 and len(BUILDS) == 30
for mission in MISSIONS:
    definition=raw_file(mission['source'])[mission['path_id']]['data']
    mission['title']['ru']=STRINGS['ru'].get(definition['_missionNameKey'],mission['title']['ru'])
    mission['description']['ru']=STRINGS['ru'].get(definition['_missionDescriptionKey'],mission['description']['ru'])

LABELS = {
    1: "Материнский корабль", 9: "Штурмовик Радаа", 10: "Перехватчик", 11: "Линейный крейсер Радаа",
    13: "Ударный бомбардировщик", 14: "Тяжёлый корвет", 15: "Штурмовой фрегат Радаа", 16: "Носитель",
    18: "Штурмовой фрегат", 19: "Ресурсный контроллер", 20: "Ионный фрегат", 21: "Тяжёлый крейсер",
    22: "Фрегат защитного поля (предварительно)", 23: "Разведчик", 24: "Многопушечный корвет", 25: "Переработчик Радаа",
    26: "Инженерный корвет", 27: "Повреждённый эсминец Радаа", 29: "Лучевой истребитель Радаа",
    30: "Эсминец", 31: "Лазерный корвет Радаа", 32: "Эсминец Радаа", 33: "Командный корвет Радаа",
    34: "Тяжёлый ракетный фрегат Радаа", 35: "Бомбардировщик Радаа", 36: "Гиперврата Радаа",
    37: "Корвет Радаа (исходный тип MissileCorvette)", 38: "Фрегат проникновения Радаа",
    39: "Тяжёлая ракетная платформа Радаа", 41: "Верфь Радаа", 43: "Верфь хиигарян", 44: "Корабль бентуси",
    45: "Баррикадный фрегат", 46: "Баллистический эсминец", 47: "Генератор щита Радаа", 48: "Башня Радаа",
    49: "Сдавшийся эсминец Радаа", 50: "Сборщик ресурсов", 51: "Shatter Station", 52: "Крыло Shatter Station",
    53: "Консоль Shatter Station", 54: "Стационарный линейный крейсер Радаа", 8: "Добывающая платформа",
}


def source(record: dict) -> str:
    return f"`{record['source']}:{record['path_id']}`"


def squadron_count(ship_type: int) -> int:
    return SHIPS[ship_type]["data"]["_staticData"]["<SquadronCount>k__BackingField"]


def ship_name(ship_type: int, technical: bool = True) -> str:
    record = SHIPS[ship_type]
    name = LABELS.get(ship_type) or STRINGS["ru"].get(record["data"].get("_nameKey")) or record["name"]
    return name + (f" (`{record['name']}`)" if technical else "")


def members(data: dict) -> collections.Counter:
    if "Type" in data:
        return collections.Counter({data["Type"]: 1})
    counts = collections.Counter(m["Type"] for m in data.get("Members", []))
    if data.get("HasUniqueMember") and data.get("UniqueMemberInit", {}).get("Type"):
        counts[data["UniqueMemberInit"]["Type"]] += 1
    return counts


def composition(counts: collections.Counter, technical: bool = True) -> str:
    if not counts:
        return "0 отрядов / 0 корпусов (пустой шаблон)"
    return "; ".join(f"{n} отр. / {n * squadron_count(t)} корп. × {ship_name(t, technical)}" for t, n in sorted(counts.items()))


def total_counts(counts: collections.Counter) -> str:
    return f"{sum(counts.values())} / {sum(n * squadron_count(t) for t, n in counts.items())}"


def spawner_description(record: dict, seen: set | None = None) -> str:
    seen = set() if seen is None else seen
    ident = (record["source"], record["path_id"])
    if ident in seen:
        return "[повторная ссылка]"
    seen = seen | {ident}
    data = record["data"]
    if record["class_name"].endswith(".PatrolManager"):
        groups = [pointer(record["source"], p) for p in data.get("_groups", [])]
        return "Патруль, один вариант: " + " / ИЛИ / ".join(spawner_description(g, seen) for g in groups if g)
    init = data.get("_data", data)
    team = {0: "нейтральная/None", 1: "игрок", 1024: "Computer1", 2048: "Computer2"}.get(init.get("TeamId"), str(init.get("TeamId")))
    if "Members" not in init and "Type" not in init:
        return f"{record['class_name']}; {source(record)}"
    return f"{team}: {composition(members(init), False)}; {source(record)}"


GRAPHS = {p.stem.removesuffix("-graph"): json.loads(p.read_text(encoding="utf-8")) for p in DATA.glob("*-graph.json")}
GRAPHS_BY_REF = {(g["source"]["source"], g["source"]["path_id"]): (name, g) for name, g in GRAPHS.items()}


def contexts(graph: dict, label: str, seen: set | None = None):
    """Include embedded graphs and referenced macro assets; no new extraction."""
    seen = set() if seen is None else seen
    ident = graph.get("_embed_identity") or (graph["source"]["source"], graph["source"]["path_id"])
    if ident in seen:
        return
    seen = seen | {ident}
    yield label, graph
    for number, node in enumerate(graph["nodes"]):
        if not node["$type"].endswith(".SubgraphUnit"):
            continue
        nest = node["nest"]
        if nest["source"] == "Embed" and nest.get("embed"):
            embed = nest["embed"]
            elements = embed["elements"]
            child = {
                "source": graph["source"], "nodes": [e for e in elements if not e["$type"].endswith((".ControlConnection", ".ValueConnection"))],
                "edges": [e for e in elements if e["$type"].endswith((".ControlConnection", ".ValueConnection"))],
                "object_references": graph["object_references"], "variables": embed.get("variables", {}),
            }
            # Embedded graphs share Unity object references but have their own IDs.
            child_label = f"{label}/embed:{node.get('$id', number)}:{embed.get('title') or 'без названия'}"
            child["_embed_identity"] = (ident, node.get("$id", number))
            yield from contexts(child, child_label, seen)
        elif nest.get("macro") is not None:
            ref = graph["object_references"][nest["macro"]]
            target = GRAPHS_BY_REF.get((ref["source"], ref["path_id"]))
            if target:
                yield from contexts(target[1], target[0], seen)


def variables(scene: dict) -> dict:
    result = {}
    for owner in scene["variables"]:
        for entry in owner["values"]["declarations"]["collection"]["$content"]:
            value = entry["value"]
            if isinstance(value, dict) and value.get("$type") == "UnityEngine.Object":
                result[entry["name"]] = owner["object_references"][value["$content"]]
    return result


def node_maps(graph: dict):
    nodes = {n["$id"]: n for n in graph["nodes"] if "$id" in n}
    value_in, control_in, control_out = collections.defaultdict(list), collections.defaultdict(list), collections.defaultdict(list)
    for e in graph["edges"]:
        a, b = e["sourceUnit"]["$ref"], e["destinationUnit"]["$ref"]
        if e["$type"].endswith(".ValueConnection"):
            value_in[b].append((e["destinationKey"], a))
        else:
            control_in[b].append(a)
            control_out[a].append(b)
    return nodes, value_in, control_in, control_out


def spawn_targets(graph: dict, scene: dict, node: dict) -> list[tuple[str, dict]]:
    nodes, value_in, _, _ = node_maps(graph)
    scene_vars = variables(scene)
    result = []

    def walk(ident: str, seen: set):
        if ident in seen:
            return
        seen = seen | {ident}
        n = nodes[ident]
        if n["$type"].endswith(".GetVariable"):
            name = n.get("defaultValues", {}).get("name", {}).get("$content")
            ref = scene_vars.get(name)
            if ref:
                result.append((name, raw_file(ref["source"])[ref["path_id"]]))
            return
        for _, parent in value_in[ident]:
            walk(parent, seen)

    for key, ident in value_in[node["$id"]]:
        if key in {"EntityInitializer", "AdditionalSpawners"}:
            walk(ident, set())
    return result


def group_label(graph: dict, node: dict) -> str:
    if not node.get("position"):
        return "—"
    p = node["position"]
    groups = [n for n in graph["nodes"] if n["$type"].endswith(".GraphGroup") and n["position"]["xMin"] <= p["x"] <= n["position"]["xMax"] and n["position"]["yMin"] <= p["y"] <= n["position"]["yMax"]]
    return ", ".join(g.get("label") or "без названия" for g in groups) or "—"


def dialogue_ref(graph: dict, node: dict) -> dict | None:
    if not node["$type"].endswith(".PlayDialogue"):
        return None
    resolved = node.get("resolved_objects", {}).get("_dialogueLine")
    if resolved:
        return resolved
    value = node.get("defaultValues", {}).get("_dialogueLine", {}).get("$content")
    if value is None:
        return None
    ref = graph["object_references"][value]
    raw = raw_file(ref["source"])[ref["path_id"]]
    return {**ref, "text_key": raw["data"]["_textKey"]}


def nearby_context(graph: dict, node: dict) -> str:
    nodes, _, incoming, _ = node_maps(graph)
    queue = [(ident, 0) for ident in incoming[node["$id"]]]
    seen, results = set(), []
    while queue and len(results) < 3:
        ident, depth = queue.pop(0)
        if ident in seen or depth > 16:
            continue
        seen.add(ident)
        n = nodes[ident]
        kind = n["$type"].split(".")[-1]
        if kind == "PlayDialogue":
            ref = dialogue_ref(graph, n)
            results.append(f"после `{ref['text_key']}` (узел {ident})")
        elif kind.startswith("On") or kind == "CustomEvent":
            args = n.get("defaultValues", {})
            resolved = n.get("resolved_objects", {})
            key = next((r.get("text_key") for r in resolved.values() if r.get("text_key")), None)
            name = args.get("name", {}).get("$content")
            results.append(f"{kind}:{ident}" + (f" `{key or name}`" if key or name else ""))
        else:
            queue += [(parent, depth + 1) for parent in incoming[ident]]
    return "; ".join(results) or "см. управляющие рёбра и метку редактора"


def bilingual(key: str) -> list[str]:
    out = []
    for lang, label in [("en", "EN — исходник Quest"), ("ru", "RU — исходная локализация Quest")]:
        text = STRINGS[lang].get(key) or f"[Строка {lang.upper()} отсутствует.]"
        out += [f"*{label}:*", "", "> " + text.replace("\n", "\n> "), ""]
    return out


def mission_info(mission: dict) -> dict:
    raw = raw_file(mission["source"])[mission["path_id"]]
    scene = json.loads((DATA / f"{mission['scene_file']}.json").read_text(encoding="utf-8"))
    name = mission["id"]
    graph = GRAPHS["Mission_M9_v2" if name == "Mission_M9" else name]
    fleet, total = [], collections.Counter()
    for field in ["default_groups", "additional_groups"]:
        for g in mission[field]:
            counts = members(g["data"])
            fleet.append({"kind": field, "name": g["name"], "counts": counts, "record": g})
            total += counts
    auto = []
    for p in scene["placements"]:
        if p["class_name"].endswith((".GroupSpawner", ".SquadronSpawner")) and p.get("auto_spawn"):
            auto.append(p)
            if p["data"].get("TeamId") == 1:
                counts = members(p["data"])
                fleet.append({"kind": "scene auto", "name": p["name"], "counts": counts, "record": p})
                total += counts
    controllers = [r for r in raw_file(mission["scene_file"]).values() if r["class_name"] == "Hercules.Designer.BuildCommandController"]
    assert len(controllers) == 1, (name, controllers)
    controller = controllers[0]
    build_list = controller["data"]["_buildCommandList"]
    listed = [pointer(controller["source"], p) for p in build_list["_buildCommands"]]
    mode = "Whitelist (1)" if build_list["_controlMode"] == 1 else "Blacklist (0)"
    if build_list["_controlMode"] == 1:
        available = [r for r in listed if not r["data"]["_debugOnly"]]
    else:
        banned = {(r["source"], r["path_id"]) for r in listed}
        available = [r for r in BUILDS if not r["data"]["_debugOnly"] and (r["source"], r["path_id"]) not in banned]
    return {"mission": mission, "raw": raw, "scene": scene, "graph": graph, "fleet": fleet, "total": total, "auto": auto, "controller": controller, "listed": listed, "available": available, "mode": mode}


def main():
    campaign = sorted([m for m in MISSIONS if m["category"] == "_campaignMissions"], key=lambda m: m["order"])
    tutorials = [m for m in MISSIONS if m["category"] == "_tutorialMissions"]
    expected_order = ["Mission_M1", "Mission_M7", "Mission_M3", "Mission_M4", "Mission_M5", "Mission_M6", "Mission_M9", "Mission_M10", "Mission_M11", "Mission_M8", "Mission_M13"]
    database_names = [pointer(DATABASE["source"], p)["name"] for p in DATABASE["data"]["_campaignMissions"]]
    assert database_names == expected_order == [m["id"] for m in campaign]
    assert len(tutorials) == 1 and tutorials[0]["id"] == "Mission_T1"
    infos = [mission_info(m) for m in campaign + tutorials]
    out = """# Quest: флот, строительная прогрессия и появления в полной кампании

Составлено по **уже извлечённой полной Quest-версии** 17 октября 2026 года. Это отдельный источник; параметры Steam-демки сюда не перенесены. Здесь 11 миссий полной кампании и T1 отдельно. Тексты всех сцен см. в `QUEST_SCENARIOS.md`; ниже — флот, ресурсы и реальные узлы скриптов.

## Как читать числа и степень подтверждения

Запись Members в GroupInitialization — слот отряда, а не обязательно один физический корпус. Размер взят **из Quest ShipDefinition**, `_staticData.<SquadronCount>k__BackingField`. Например, перехватчик/бомбардировщик — по 5 корпусов в отряде, разведчик — 3, инженер — 1. Таблицы показывают оба числа.

**Carryover=true:** DefaultGroups и DefaultRU — резервный/начальный состав определения, а не гарантированное фактическое состояние обычного прохождения. Фактические корабли и RU зависят от выжившего флота предыдущей главы, AdditionalGroups, уровня сложности и правил переноса. Поэтому численный baseline ниже — DefaultGroups + AdditionalGroups + автоматические дружеские размещения карты **без выдуманного состояния сохранения**. AdditionalRU и MinimumCatchupValue приведены отдельно.

Числа, ссылки, whitelist/blacklist-поля, графы и их рёбра прочитаны из Quest-ассетов. Код из `decompiled-demo` используется только как **вспомогательная модель значения имён классов/полей**, а не как доказательство побайтно одинакового исполнения другой версии. В частности, предполагаемая семантика режимов BuildCommandList (1=Whitelist, 0=Blacklist), debug-флага и Carryover соответствует этой модели и согласуется с содержимым списков. Игровой запуск Quest здесь не проводился.

В сыром Quest-аудите есть ошибки чтения некоторых VFX/HUD/AbilityDefinition; используемые здесь MissionDatabase, MissionDefinition, ShipDefinition, BuildDefinition, ObjectiveDefinition и графы прочитаны. Отсутствие совместимости AbilityDefinition не подменено способностями Steam-версии.

## Порядок MissionDatabase и стартовые параметры

Порядок ниже задан `_campaignMissions`, а не сортировкой номеров M*. T1 хранится отдельно в `_tutorialMissions`.

| № | Миссия | DefaultRU | FleetCap | Carryover | AdditionalRU | MinimumCatchupValue | Baseline: отрядов/корпусов | Типов по стартовому BuildController |
|---:|---|---:|---:|---|---:|---:|---:|---:|
""".splitlines()
    for i, p in enumerate(infos):
        m, d = p["mission"], p["raw"]["data"]
        number = str(i + 1) if i < 11 else "отдельно"
        out.append(f"| {number} | {m['id']} — {m['title']['ru'] or m['title']['en']} | {m['starting_ru']} | {m['fleet_cap']} | {m['carryover']} | {d['<AdditionalRU>k__BackingField']} | {d['<MinimumCatchupValue>k__BackingField']} | {total_counts(p['total'])} | {len(p['available'])} |")
    out += ["", f"Источник порядка: MissionDatabase {source(DATABASE)}. BuildController показывает начальную настройку списка; в M7 и M9 строительство затем блокируется/восстанавливается отдельными узлами.", "", "## Что здесь является исследованием", "", "В этих данных **не обнаружено отдельной очереди оплачиваемых Research-технологий** с ценой, длительностью и зависимостями, подобной HWRM. Найдены реальные **скриптовые открытия/восстановления строительства** и сюжетные объявления новых корпусов. Это нужно переносить как правила миссии/разрешение постройки либо сознательно превратить в исследования HWRM при адаптации.", "", "Подтверждённые управляющими рёбрами примеры:", "", "- **M7:** `DisableBuildSystem:219` после `OnSimReady:194`. После цели `M07_Objective_02a` («Harvest 2000 total RU to restore construction sytems.»), событие `OnObjectiveCompleted:251` идёт в `SetBuildByBuildList:337`, `_enable=true`, `CanScrap=true`.", "- **M9:** во вступительной цепочке есть `DisableBuildSystem:313`. После передачи технологий Бентуси, реплика `M09_020_060_BN` (`Mission_M9_v2:587`) ведёт в `SetBuildByBuildList:205`, `_enable=true`, `CanScrap=true`.", "- Объявления `FI_Unlock*` действительно подключены в графах, однако обычно новый тип уже включён в список соответствующей сцены. Реплика сама по себе не равна отдельному платному исследованию; ниже указаны и граф, и строительный список.", ""]
    unlocks = []
    spawn_rows = 0
    unresolved = []
    for i, p in enumerate(infos):
        m, d = p["mission"], p["raw"]["data"]
        heading = f"{i + 1}. {m['id']}" if i < 11 else "Отдельно: Mission_T1"
        out += [f"## {heading} — {m['title']['ru'] or m['title']['en']}", "", f"Определение: {source(p['raw'])}; карта `{m['scene_file']}`; граф `{p['graph']['source']['name']}` — {source(p['graph']['source'])}.", "", f"DefaultRU **{m['starting_ru']}**, FleetCap **{m['fleet_cap']}**, Carryover **{m['carryover']}**, AdditionalRU **{d['<AdditionalRU>k__BackingField']}**, MinimumCatchupValue **{d['<MinimumCatchupValue>k__BackingField']}**.", "", "### DefaultGroups, AdditionalGroups и автоматические размещения", "", "DefaultGroups при включённом переносе — baseline для случая без полученного флота, не утверждение о фактических выживших кораблях.", "", "| Откуда | Группа | Состав: отряды / корпуса | Источник |", "|---|---|---|---|"]
        for f in p["fleet"]:
            out.append(f"| {f['kind']} | `{f['name']}` | {composition(f['counts'])} | {source(f['record'])} |")
        other_auto = [r for r in p["auto"] if r["data"].get("TeamId") != 1]
        for r in other_auto:
            out.append(f"| scene auto, команда {r['data'].get('TeamId')} | `{r['name']}` | {composition(members(r['data']))} | {source(r)} |")
        out += ["", f"Baseline игрока (без других команд): **{total_counts(p['total'])} отрядов/корпусов**. Неуправляемые объекты и нейтральные цели не добавлены в это число.", "", "### Строительный список", "", f"BuildCommandController {source(p['controller'])}; режим **{p['mode']}**. Явный список: " + ", ".join(f"`{r['name']}`" for r in p["listed"]) + ".", "", "| Тип по исходному списку | Отряд/корпусов | RU | `_duration` | BuildDefinition |", "|---|---:|---:|---:|---|"]
        for r in p["available"]:
            bd = r["data"]
            out.append(f"| {ship_name(bd['_shipType'])} | 1/{squadron_count(bd['_shipType'])} | {bd['_cost']} | {bd['_duration']:g} | `{r['name']}`, {source(r)} |")
        out += ["", "Цена относится к строительной записи/отряду, а не автоматически к одному физическому корпусу. `_duration` — исходное поле Quest; ускорение при планировании и другие исполнительные детали требуют проверки этой версии.", "", "### Подключённые изменения доступности и выдачи RU", "", "| Граф:узел | Действие и параметры | Управляющий контекст |", "|---|---|---|"]
        changes = 0
        all_contexts = list(contexts(p["graph"], p["graph"]["source"]["name"]))
        seen_contexts = set()
        for label, graph in all_contexts:
            if label in seen_contexts:
                continue
            seen_contexts.add(label)
            _, _, incoming, outgoing = node_maps(graph)
            for n in graph["nodes"]:
                kind = n["$type"].split(".")[-1]
                ident = n.get("$id")
                connected = bool(ident and (incoming[ident] or outgoing[ident]))
                if kind in {"SetBuildByBuildList", "DisableBuildSystem", "AddRU"} and connected:
                    args = {k: v.get("$content", v) if isinstance(v, dict) else v for k, v in n.get("defaultValues", {}).items()}
                    out.append(f"| `{label}:{ident}` | {kind}: `{json.dumps(args, ensure_ascii=False)}` | {nearby_context(graph, n)} |")
                    changes += 1
                if kind == "PlayDialogue":
                    ref = dialogue_ref(graph, n)
                    if ref and ref["text_key"].startswith("FI_Unlock"):
                        unlocks.append({"mission": m["id"], "label": label, "id": ident or n.get("guid"), "key": ref["text_key"], "connected": connected, "context": nearby_context(graph, n) if connected else "нет управляющих связей", "ref": ref})
        if not changes:
            out.append("| — | Подключённых SetBuildByBuildList / DisableBuildSystem / AddRU не найдено | Новые корпуса см. в списке и репликах ниже |")
        out += ["", "### Дружеские подкрепления и противники, создаваемые сценарием", "", "Состав указан **за одно срабатывание** SpawnEntity. Если PatrolManager содержит варианты, выбирается один вариант, а не сумма всех. Таймеры и условия могут повторять появления. Метка редактора и ближайшее событие служат навигацией, а не заменяют полный порядок исполнения графа.", "", "| Граф:узел / метка | Спавнер | Состав и команда |", "|---|---|---|"]
        count_spawns = 0
        for label, graph in all_contexts:
            _, _, incoming, outgoing = node_maps(graph)
            for n in graph["nodes"]:
                if not n["$type"].endswith(".SpawnEntity"):
                    continue
                ident = n.get("$id")
                if not ident or not (incoming[ident] or outgoing[ident]):
                    continue
                targets = spawn_targets(graph, p["scene"], n)
                if not targets:
                    unresolved.append(f"{m['id']}:{label}:{ident}")
                    out.append(f"| `{label}:{ident}` — {group_label(graph, n)} | [Цель требует ручной сверки value-рёбер] | {nearby_context(graph, n)} |")
                for alias, target in targets:
                    out.append(f"| `{label}:{ident}` — {group_label(graph, n)} | `{alias}`, {source(target)} | {spawner_description(target)} |")
                    count_spawns += 1
        if not count_spawns:
            out.append("| — | Нет подключённого SpawnEntity с разрешённой целью | См. автоматические размещения сцены |")
        spawn_rows += count_spawns
        out += ["", "### Объявление нового корпуса", ""]
        mission_unlocks = [u for u in unlocks if u["mission"] == m["id"]]
        if not mission_unlocks:
            out += ["Подключённой реплики FI_Unlock* в этом миссионном графе не найдено. Сюжетные упоминания ремонта/технологий не приравнены к исследованию.", ""]
        for u in mission_unlocks:
            out += [f"**`{u['key']}`**, `{u['label']}:{u['id']}`; управляющие связи: **{u['connected']}**. {u['context']}. DialogueLine {source(u['ref'])}.", ""] + bilingual(u["key"])
    assert len([u for u in unlocks if u["connected"]]) == 9
    out += ["## Сводка подключённых объявлений и карта строительного открытия", "", "| По порядку кампании | Объявление | Подключённый узел |", "|---|---|---|"]
    for u in unlocks:
        if u["connected"]:
            out.append(f"| {u['mission']} | `{u['key']}` | `{u['label']}:{u['id']}` |")
    out += ["", "Все девять объявлений имеют управляющие рёбра. Их содержимое — новые корпуса, инженерные работы, захваченные планы или передачи Бентуси. Для HWRM эти этапы можно отобразить через разрешения build/research, но это будет адаптация к механике HWRM, а не найденная исходная Research-очередь.", "", "### Буквальные реплики, сопровождающие реальное восстановление M7/M9", ""]
    for key in ["M07_Objective_02a", "M07_030_050_KS", "M07_040_010_TS", "M09_020_060_BN", "M09_020_070_KS"]:
        out += [f"**`{key}`**", ""] + bilingual(key)
    out += ["## Ограничения и воспроизводимость", "", f"В исходном аудите зафиксировано **{len(INDEX['failures'])} ошибок чтения**; это не число потерянных миссий. В этой работе использованы прочитанные 12 MissionDefinition, 46 ShipDefinition, 30 BuildDefinition, MissionDatabase, доступные миссионные/патрульные графы, размещения и строки. Всего в таблицах разрешено **{spawn_rows} ссылок на подключённые цели SpawnEntity**; одна строка не означает уникальную волну.", ""]
    if unresolved:
        out += ["Не разрешённые автоматически цели value-рёбер:", ""] + [f"- `{x}`" for x in unresolved] + [""]
    else:
        out += ["Цели всех перечисленных подключённых SpawnEntity разрешены по SceneVariables и value-рёбрам, включая встроенные подграфы. Существование Patrol_Setup/GlobalAchievements-макросов учитывается, но команды Patrol не пересчитаны как новые корабли.", ""]
    out += ["Источник данных — `local/quest-campaign` и `local/quest-audit`; ссылки `32hex:path_id` относятся к **Quest-файлам**, не к `resources.assets` Steam. Генератор — `tools/write_quest_progression.py`. Он читает существующую выгрузку и пишет только этот документ; игры, мод и Steam-файлы не изменяет.", "", "Для проверки фактического начала миссии с переносом необходимы конкретное сохранение и сложность. Неиспользуемые шаблоны, disconnected AddRU/PlayDialogue и нейтральные объекты не объявлены бесплатным боевым флотом. Отдельное отсутствие Research-очереди — вывод по найденным структурам и графам, не утверждение о невозможности любой иной реализации в нечитаемых участках версии.", ""]
    path = ROOT / "docs/QUEST_PROGRESSION.md"
    path.parent.mkdir(exist_ok=True)
    path.write_text("\n".join(out), encoding="utf-8")
    print(json.dumps({"document": str(path), "campaign_missions": 11, "tutorial_missions": 1, "connected_unlock_announcements": len([u for u in unlocks if u["connected"]]), "spawn_target_rows": spawn_rows, "unresolved_spawn_nodes": unresolved, "raw_failures": len(INDEX['failures'])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
