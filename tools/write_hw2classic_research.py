"""Write a design reference from extracted Classic data; no mod/game changes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from audit_hw2classic_balance import BASE, ROOT, tables


TARGETS = {
    "hgn_mothership": "Материнский корабль / Mothership",
    "hgn_carrier": "Носитель / Carrier",
    "hgn_shipyard": "Верфь / Shipyard",
    "hgn_scout": "Разведчик / Scout",
    "hgn_interceptor": "Перехватчик / Interceptor",
    "hgn_attackbomber": "Штурмовой бомбардировщик / Bomber",
    "hgn_assaultcorvette": "Штурмовой корвет / Gunship",
    "hgn_pulsarcorvette": "Корвет-пульсар / Pulsar Gunship",
    "hgn_minelayercorvette": "Минный корвет / Minelayer Corvette",
    "hgn_torpedofrigate": "Торпедный фрегат / Torpedo Frigate",
    "hgn_assaultfrigate": "Зенитный фрегат / Flak Frigate",
    "hgn_ioncannonfrigate": "Ионный фрегат / Ion Cannon Frigate",
    "hgn_marinefrigate": "Десантный фрегат / Marine Frigate",
    "hgn_defensefieldfrigate": "Фрегат защитного поля / Defense Field Frigate",
    "hgn_destroyer": "Эсминец / Destroyer",
    "hgn_battlecruiser": "Линейный крейсер / Battlecruiser",
    "hgn_gunturret": "Пушечная платформа / Gun Platform",
    "hgn_ionturret": "Ионная платформа / Ion Beam Platform",
    "hgn_resourcecollector": "Сборщик ресурсов / Resource Collector",
    "hgn_resourcecontroller": "Ресурсный контроллер / Mobile Refinery",
    "hgn_proximitysensor": "Датчик приближения / Proximity Sensor",
    "hgn_ecmprobe": "Зонд-помехопостановщик / Sensors Distortion Probe",
    "vgr_mothership": "Флагман / Flagship",
    "vgr_carrier": "Носитель / Carrier",
    "vgr_shipyard": "Верфь / Shipyard",
    "vgr_scout": "Разведчик / Scout",
    "vgr_interceptor": "Штурмовик / Assault Craft",
    "vgr_bomber": "Бомбардировщик / Bomber",
    "vgr_lancefighter": "Лучевой истребитель / Lance Fighter",
    "vgr_missilecorvette": "Ракетный корвет / Missile Corvette",
    "vgr_lasercorvette": "Лазерный корвет / Laser Corvette",
    "vgr_commandcorvette": "Командный корвет / Command Corvette",
    "vgr_minelayercorvette": "Минный корвет / Minelayer Corvette",
    "vgr_assaultfrigate": "Штурмовой фрегат / Assault Frigate",
    "vgr_heavymissilefrigate": "Тяжёлый ракетный фрегат / Heavy Missile Frigate",
    "vgr_infiltratorfrigate": "Десантный фрегат / Infiltrator Frigate",
    "vgr_destroyer": "Эсминец / Destroyer",
    "vgr_battlecruiser": "Линейный крейсер / Battlecruiser",
    "vgr_weaponplatform_gun": "Пушечная платформа / Gun Platform",
    "vgr_weaponplatform_missile": "Ракетная платформа / Missile Platform",
    "vgr_hyperspace_platform": "Гиперпространственные врата / Hyperspace Gate",
    "vgr_resourcecollector": "Сборщик ресурсов / Resource Collector",
    "vgr_probe_prox": "Датчик приближения / Proximity Sensor Probe",
    "vgr_probe_ecm": "Зонд-помехопостановщик / Sensors Distortion Probe",
    "fighter": "Истребители / Fighter class",
    "corvette": "Корветы / Corvette class",
    "frigate": "Фрегаты / Frigate class",
    "capital": "Крупные корабли / Capital class",
    "platform": "Платформы / Platform class",
    "utility": "Вспомогательные корабли / Utility class",
}
SPECIAL = {
    "GraviticAttractionMines": "Укладка мин / Minelaying Technology",
    "PlatformIonWeapons": "Ионные орудия платформ / Platform Ion Weapons",
    "DestroyerTech": "Шасси эсминца / Destroyer Chassis",
    "BattlecruiserIonWeapons": "Шасси линейного крейсера / Battlecruiser Chassis",
    "ECMProbe": "Зонд-помехопостановщик / Sensors Distortion Probe",
    "SensDisProbe": "Датчик приближения / Proximity Sensor",
    "RepairAbility": "Ремонтные системы / Repair Systems",
    "ScoutPingAbility": "Пинг разведчика / Enhanced Scout Sensors",
    "ImprovedTorpedo": "Тяжёлые торпеды / Improved Torpedoes",
    "AttackBomberImprovedBombs": "Противоподсистемные бомбы / Improved Bombs",
    "BomberImprovedBombs": "Противоподсистемные бомбы / Improved Bombs",
    "ScoutEMPAbility": "Электромагнитное оружие / EMP",
    "DefenseFieldFrigateShield": "Защитное поле / Defense Field",
    "CorvetteTech": "Шасси корветов / Corvette Chassis",
    "FrigateTech": "Шасси фрегатов / Frigate Chassis",
    "ProbeSensorDisruption": "Зонд-помехопостановщик / Sensors Distortion Probe",
    "ProbeProxSensor": "Датчик приближения / Proximity Sensor Probe",
    "LanceBeams": "Лучевое оружие / Lance Beams",
    "PlasmaBombs": "Плазменные бомбы / Plasma Bombs",
    "CorvetteGraviticAttraction": "Минные системы / Corvette Minelaying Systems",
    "CorvetteLaser": "Лазерные системы / Corvette Laser Systems",
    "CorvetteCommand": "Командные системы / Command Corvette Systems",
    "PlatformHeavyMissiles": "Тяжёлые ракеты платформ / Platform Heavy Missiles",
    "FrigateAssault": "Штурмовые фрегаты / Assault Frigate Technology",
    "FrigateInfiltrationTech": "Абордажные технологии / Infiltration Technology",
    "DestroyerGuns": "Шасси эсминца / Destroyer Chassis",
    "HyperspaceGateTech": "Гиперпространственные врата / Hyperspace Gate Technology",
}
MODULES = (
    ("production_fighter", "Производство истребителей / Fighter Facility"),
    ("production_corvette", "Производство корветов / Corvette Facility"),
    ("production_frigate", "Производство фрегатов / Frigate Facility"),
    ("production_capship", "Производство крупных кораблей / Capital Ship Facility"),
    ("module_platformcontrol", "Управление платформами / Platform Control Module"),
    ("module_research", "Наука / Research Module"),
    ("module_researchadvanced", "Продвинутая наука / Advanced Research Module"),
    ("module_hyperspace", "Гиперпространство / Hyperspace Module"),
    ("module_hyperspaceinhibitor", "Подавление гиперпрыжков / Gravity Well Generator"),
    ("module_cloakgenerator", "Маскировка / Cloak Generator"),
    ("module_firecontrol", "Координация огня / Fire Control Tower"),
    ("sensors_advancedarray", "Сенсорная батарея / Advanced Sensors Array"),
    ("sensors_detecthyperspace", "Гиперпространственные сенсоры / Hyperspace Sensors"),
    ("sensors_detectcloaked", "Обнаружение маскировки / Anti-Cloaking Sensors"),
)


def source_record(path):
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def state(row):
    if "RESEARCH HACK" in row.get("RequiredResearch", ""): return "script_only"
    if row["Name"] == "InstaAdvancedFrigateTech": return "automatic_internal"
    if row["Name"] in ("DamageMoverTech", "RadiationDefenseField"): return "campaign_only"
    return "normal"


def cell(value):
    return str(value or "—").replace("|", "\\|").replace("\n", " ")


def label(row):
    name = row["Name"]
    if name in SPECIAL: return SPECIAL[name]
    kind = {"MAXHEALTH": "Прочность / Hull", "MAXSPEED": "Скорость / Engine",
            "BUILDSPEED": "Производство / Improved Manufacturing", "HyperspaceCost": "Стоимость гиперпрыжка / Hyperspace Cost"}.get(row.get("UpgradeName"))
    if kind: return kind + (" I" if name.endswith("1") else " II" if name.endswith("2") else "")
    return name


def export():
    output = {"source": "Extracted Steam Homeworld 2 Classic Lua4 data, not HWRM", "engine_tested": False,
              "ten_articles": ["https://www.homeworld3.ru/index.php?name=Pages&op=page&pid=95", "https://www.homeworld3.ru/index.php?name=Pages&op=page&pid=96"], "races": {}}
    for race, prefix in (("hiigaran", "hgn"), ("vaygr", "vgr")):
        research_path = BASE / "scripts/building and research" / race / "research.lua"
        build_path = research_path.with_name("build.lua")
        research = list(tables(research_path)[0]["research"].values())
        build = list(tables(build_path)[0]["build"].values())
        modules = {}
        for row in build:
            if row["Type"] != 1: continue
            ident = row["ThingToBuild"].lower()
            path = BASE / "subsystem" / ident / (ident + ".subs")
            values, _ = tables(path)
            config = next(v for v in values.values() if isinstance(v, dict))
            modules[ident] = {**source_record(path), "config": config, "build": row}
        output["races"][race] = {"research_source": source_record(research_path), "build_source": source_record(build_path),
                                  "research": [{"scope": state(row), "raw": row} for row in research], "build": build, "modules": modules}
    target = ROOT / "local/novokushan/hw2classic-research.json"
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = ROOT / "docs/HW2_CLASSIC_RESEARCH.md"
    header = (ROOT / "docs/reference/HW2_CLASSIC_RESEARCH_OVERVIEW.md").read_text(encoding="utf-8")
    lines = [header, "", "## Исходные модули: цена и базовое время", "", "Модули Материнского корабля/Флагмана. Требования приведены в исходном синтаксисе; F — подсистемы флота, R — уже полученные технологии. Стоимость модулей носителей сохранена отдельно в JSON.", "", "| Модуль RU / EN | Хиигаряне RU / с | Допуск Hgn | Вэйгры RU / с | Допуск Vgr |", "|---|---:|---|---:|---|"]
    for suffix, name in MODULES:
        cells = [name]
        for race, prefix in (("hiigaran", "hgn"), ("vaygr", "vgr")):
            row = output["races"][race]["modules"].get(prefix + "_ms_" + suffix)
            if row:
                config, build = row["config"], row["build"]
                cells += [f'{config["costToBuild"]} / {config["timeToBuild"]}', cell("; ".join(k + ": " + build[key] for k, key in (("F", "RequiredFleetSubSystems"), ("R", "RequiredResearch")) if build.get(key)))]
            else: cells += ["—", "—"]
        lines.append("| " + " | ".join(cells) + " |")
    lines += ["", "## Полная таблица обычных исследований", "", "Все суммы и времена ниже считаны из локального Classic. Время — поле Time до ускорения. Множители второго уровня указаны относительно исходного состояния, не перемножаются с первым. У хиигарян R означает Research, AR — AdvancedResearch; исходные условия с & и | сохранены буквально.", ""]
    for race, title in (("hiigaran", "Хиигаряне"), ("vaygr", "Вэйгры")):
        lines += ["### " + title, "", "| Исследование RU / EN | Объект RU / EN | RU | Базовые с | Предыдущее исследование | Подсистемы | Эффект / технический ID |", "|---|---|---:|---:|---|---|---|"]
        for item in output["races"][race]["research"]:
            if item["scope"] != "normal": continue
            row = item["raw"]
            effect = str(row["UpgradeValue"]) + " × " + row["UpgradeName"] + "; " if "UpgradeValue" in row else ""
            effect += "`" + row["Name"] + "`"
            values = [label(row), TARGETS.get(row.get("TargetName", "").lower(), row.get("TargetName", "")), row["Cost"], row["Time"], row.get("RequiredResearch", ""), row.get("RequiredSubSystems", ""), effect]
            lines.append("| " + " | ".join(cell(v) for v in values) + " |")
    lines += ["", "## Кампания и внутренние условия", "", "- `InstaAdvancedFrigateTech`: 0 RU / 0 с, условие AdvancedResearch. Бесплатный внутренний допуск к зенитному, ионному и десантному фрегатам, а не отдельная платная ступень дерева.", "- `DamageMoverTech`: 500 RU / 60 с; `RadiationDefenseField`: 500 RU / 60 с — кампанийные открытия хиигарян, не обычная ветка скирмиша.", "- Все строки с RequiredResearch=`RESEARCH HACK` сохранены в JSON как script_only. Это сценарные модификаторы, не предлагаемые игроку технологии.", "", "## Расхождения с таблицей Тена", "", "Ориентир статьи — Classic 1.1, с отдельно отмеченными отличиями 1.0. Локальные данные относятся к установленной Steam-редакции Classic; полное совпадение с историческим патчем 1.1 не предполагается автоматически.", "", "- По локальному build.lua датчик приближения Hgn требует `SensDisProbe`: 500 RU / 35 с и Research; ECM-зонд требует `ECMProbe`: 500 RU / 45 с и AdvancedResearch. У Тена эти две пары цены/времени и условий распределены иначе. Здесь сохранена связь из build.lua, несмотря на вводящие в заблуждение внутренние имена.", "- В статье броня верфи Hgn — 500/750 RU, двигатели — 500/750. Локально: броня 750/1500 RU, двигатели 500/1500; подробные времена выше.", "- Гиперпространственное улучшение II Hgn локально имеет UpgradeValue=0.6; у Тена итоговое снижение описано как45%. В справочнике не подменяем исходный коэффициент описанием.", "", "## Воспроизведение и границы проверки", "", "`python -X utf8 tools/write_hw2classic_research.py` читает уже извлечённые Lua4-таблицы через существующий ограниченный декодер данных. Не исполняет игровой код, не меняет мод/релиз/установку и не запускает игру. SHA256 и полные исходные поля обеих рас: [hw2classic-research.json](../local/novokushan/hw2classic-research.json).", ""]
    lines.insert(lines.index("## Воспроизведение и границы проверки") - 1,
                 "- EMP разведчика Vgr: локально1000 RU /70 с; в статье1500 RU /70 с. Основные открытия классов/кораблей и стоимость производственных модулей совпадают.")
    report.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"report": str(report), "data": str(target), "normal_research": {race: sum(item["scope"] == "normal" for item in data["research"]) for race, data in output["races"].items()}, "game_changed": False}, ensure_ascii=False))


if __name__ == "__main__": export()
