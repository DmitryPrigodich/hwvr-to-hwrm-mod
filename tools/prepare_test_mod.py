"""Assemble two playable races using demo models and adapted HWRM combat."""

import argparse
import json
import re
import shutil
from pathlib import Path

from fleet import FLEET
from prepare_catalogue_mod import prepare as prepare_catalogue
from physical_display import configure
from model_size import native_path
from prepare_ship_icons import prepare as prepare_icons


def table_blocks(text, section):
    """Read balanced native event-table entries, ignoring Lua line comments."""
    text = re.sub(r'--[^\n]*', '', text)
    start = re.search(rf'\b{section}\s*=\s*\{{', text).end()
    depth, end = 1, start
    while depth:
        if text[end] == '{': depth += 1
        if text[end] == '}': depth -= 1
        end += 1
    section_text = text[start:end-1]
    cursor = 0
    while match := re.search(r'\w+\s*=\s*\{', section_text[cursor:]):
        begin = cursor + match.end()-1
        depth, finish = 1, begin+1
        while depth:
            if section_text[finish] == '{': depth += 1
            if section_text[finish] == '}': depth -= 1
            finish += 1
        yield section_text[begin:finish]
        cursor = finish


def combat_events(native_events, native_ship, weapons):
    # Keep death/damage effects on Root; remap fire effects to each actual muzzle.
    events = re.sub(r'(\{\s*"marker",\s*)"[^"]*"', r'\1"Root"', native_events)
    configurations = re.findall(
        r'StartShipWeaponConfig\(NewShipType,"([^"]+)","[^"]+","([^"]+)"', native_ship)
    for i, weapon in enumerate(weapons):
        animation = next((a for w,a in configurations if w == weapon), None)
        if i == 0 and animation:
            for block in table_blocks(native_events, "events"):
                if re.search(rf'"anim",\s*"{re.escape(animation)}"', block):
                    old = re.sub(r'(\{\s*"marker",\s*)"[^"]*"', r'\1"Root"', block)
                    new = re.sub(r'(\{\s*"marker",\s*)"[^"]*"', r'\1"Weapon_Gun0_Muzzle"', block)
                    events = events.replace(old, new)
        new_name = f"VR_Fire{i}"
        source = next((a for a in table_blocks(native_events, "animations")
                       if re.search(rf'name\s*=\s*"{re.escape(animation or "")}"', a)), None)
        if source:
            source = re.sub(r'name\s*=\s*"[^"]*"', f'name="{new_name}"', source, count=1)
        else:
            source = f'{{name="{new_name}",length=0.5,loop=0,parent="",minimum=0,maximum=0,markers={{""}}}}'
        events += f'\neffects.animations.animation{1000+i} = {source}\n'
        for j, block in enumerate(table_blocks(native_events, "events")):
            if not animation or not re.search(rf'"anim",\s*"{re.escape(animation)}"', block):
                continue
            block = re.sub(r'("anim",\s*)"[^"]+"', rf'\1"{new_name}"', block)
            block = re.sub(r'("marker",\s*)"[^"]+"', rf'\1"Weapon_Gun{i}_Muzzle"', block)
            events += f'effects.events.event{1000+100*i+j} = {block}\n'
    return events


def prepare(destination: Path):
    project = Path(__file__).resolve().parent.parent
    base_data = project / "local/hwrm-base"
    for race, inherited in (("novokushan", "kushan"), ("radaa", "vaygr")):
        shutil.copytree(base_data / "scripts/races" / inherited,
                        destination / "scripts/races" / race, dirs_exist_ok=True)
    shutil.copytree(project / "mod", destination, dirs_exist_ok=True)
    translations = {"English": {9901000: "Novokushan", 9901001: "Radaa"},
                    "Russian": {9901000: "Новокушане", 9901001: "Радаа"}}
    for i, ship in enumerate(FLEET, 1):
        translations["English"][9901100+i] = (
            f'{i}/8: {ship["en"]}. LEFT: VR. RIGHT: stock Remastered. Camera: keys 1-8.')
        translations["Russian"][9901100+i] = (
            f'{i}/8: {ship["ru"]}. СЛЕВА: VR. СПРАВА: штатный Remastered. Камера: клавиши 1-8.')
    for ship in FLEET:
        model_dir = project / "exports" / ship["mesh"].lower()
        reference_dir = project / "local/hw2ships/ship" / ship["archetype"]
        template = (reference_dir / (ship["archetype"]+".ship")).read_text(encoding="utf-8-sig")
        native_ship = template
        template = "\n".join(line for line in template.splitlines() if not re.match(
            r"\s*(StartShipWeaponConfig|setEngineTrail|setEngineBurn|setEngineGlow|loadLatchPointList)\(", line))
        batch = re.search(r'NewShipType.buildBatch=getShipNum\([^\n]+,\s*(\d+)\)', template)
        cost = re.search(r'NewShipType.buildCost=(\d+)', template)
        if batch and cost:
            template = re.sub(r'NewShipType.buildCost=.*',
                              f'NewShipType.buildCost={round(int(cost[1])/int(batch[1]))}', template)
        for prop, value in (("displayedName", f'"${ship["ucs"]}"'),
                            ("sobDescription", f'"${ship["ucs"]+1}"'),
                            ("BuildFamily", f'"{ship["family"]}"')):
            template = re.sub(rf'NewShipType.{prop}=.*', f'NewShipType.{prop}={value}', template)
        template += '\nNewShipType.buildBatch=1\nNewShipType.SquadronSize=1\n'
        for i, weapon in enumerate(ship["weapons"]):
            native_animation = re.search(rf'StartShipWeaponConfig\(NewShipType,"{weapon}","[^"]+","([^"]+)"', native_ship)
            animation = native_animation[1] if i == 0 and native_animation else f"VR_Fire{i}"
            template += f'StartShipWeaponConfig(NewShipType,"{weapon}","Weapon_Gun{i}","{animation}");\n'
        rig = json.loads((model_dir/"extraction.json").read_text(encoding="utf-8"))["rig"]
        for i in range(len(rig["engines"])):
            template += f'setEngineTrail(NewShipType,{i},4,"trail_ribbon.tga",0.001,0.5,0.025,6);\n'
        template += 'setEngineBurn(NewShipType,12,0.5,1,12,0,0.7,0.1,25);\n'
        # Hull latch points are not authored yet. Do not advertise unsupported abilities.
        template = "\n".join(line for line in template.splitlines() if not any(
            f'"{ability}"' in line for ability in ("CanBeCaptured", "CanBeSalvageCaptured", "CanBeRepaired")))
        ship_dir = destination / "ship" / ship["id"]
        ship_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(model_dir/"ship.hod", ship_dir/(ship["id"]+".hod"))
        (ship_dir/(ship["id"]+".ship")).write_text(configure(template)+"\n", encoding="utf-8")
        events = (reference_dir/(ship["archetype"]+".events")).read_text(encoding="utf-8-sig")
        events = combat_events(events, native_ship, ship["weapons"])
        (ship_dir/(ship["id"]+".events")).write_text(events, encoding="utf-8")
        for language, field in (("English", "en"), ("Russian", "ru")):
            translations[language][ship["ucs"]] = ship[field]
            translations[language][ship["ucs"]+1] = (
                "Модель Vast Reaches. Вооружение и лётные характеристики адаптированы из HWRM."
                if language == "Russian" else "Vast Reaches model. Combat and flight adapted from HWRM.")

    additional = prepare_catalogue(destination, translations)
    # Reference hulls must use the same physical-size display as the imported hulls.
    # Their geometry and textures continue to load from the installed game archives.
    gallery_manifest=project/'local/gallery-manifest.json'
    if gallery_manifest.exists():
        for native in {e['native'] for e in json.loads(gallery_manifest.read_text(encoding='utf-8')) if e['native']}:
            source=native_path(native);folder=destination/'ship'/native;folder.mkdir(parents=True,exist_ok=True)
            template=source.with_suffix('.ship').read_text(encoding='utf-8-sig')
            (folder/(native+'.ship')).write_text(configure(template),encoding='utf-8')
            if 'gallery-native' in source.parts:
                shutil.copyfile(source,folder/(native+'.hod'))
    gallery_labels = project/'local/gallery-labels.json'
    if gallery_labels.exists():
        for key,value in json.loads(gallery_labels.read_text(encoding='utf-8')).items():
            for language in translations:translations[language][int(key)] = value
    playable = FLEET + additional
    prepare_icons(destination)
    for race, inherited in (("novokushan", "kushan"), ("radaa", "vaygr")):
        roster = [s for s in playable if s["race"] == race]
        build = f'dofilepath("data:scripts/races/{inherited}/scripts/def_build.lua")\n'
        for priority, ship in enumerate(roster, 1):
            build += ('local nextEntry = 1\nwhile build[nextEntry] ~= nil do nextEntry = nextEntry + 1 end\n'
                      'build[nextEntry] = { Type = Ship, '
                      f'ThingToBuild = "{ship["id"]}", RequiredResearch = "", RequiredShipSubSystems = "", '
                      f'DisplayPriority = {priority}, DisplayedName = "${ship["ucs"]}", Description = "${ship["ucs"]+1}" }}\n')
        (destination/"scripts/races"/race/"scripts/def_build.lua").write_text(build, encoding="utf-8")
        prefix = "Kus" if race == "novokushan" else "Vgr"
        available={s['id'] for s in additional}
        mother='nku_mothership' if race=='novokushan' and 'nku_mothership' in available else f'{prefix}_MotherShip'
        carrier=('nku_carrier' if race=='novokushan' else 'rad_carrier')
        if carrier not in available:carrier=f'{prefix}_Carrier'
        collector='nku_resourcecollector' if race=='novokushan' and 'nku_resourcecollector' in available else f'{prefix}_ResourceCollector'
        starting = ('PersistantData = { StrikeGroups = {}, Squadrons = {\n'
                    f'{{type="{mother}",subsystems={{}},shiphold={{}},name="",size=1}},\n'
                    f'{{type="{carrier}",subsystems={{}},shiphold={{}},name="",size=1}},\n'
                    f'{{type="{collector}",subsystems={{}},shiphold={{}},name="",size=1,number=6}},\n')
        for ship in [s for s in FLEET if s['race']==race]:
            count = 1 if "Frigate" in ship["family"] else 3
            starting += f'{{type="{ship["id"]}",subsystems={{}},shiphold={{}},name="",size=1,number={count}}},\n'
        starting += '}, Research = {} }\n'
        (destination/"scripts/startingfleets"/(race+"00.lua")).write_text(starting, encoding="utf-8")
    for language, entries in translations.items():
        folder = destination / "locale" / language
        folder.mkdir(parents=True, exist_ok=True)
        (folder/"vastreaches.ucs").write_text(
            "".join(f"{key}\t{value}\r\n" for key,value in sorted(entries.items())), encoding="utf-16", newline="")
    (destination/"fleet-manifest.json").write_text(json.dumps(playable, ensure_ascii=False, indent=2), encoding="utf-8")
    # Isolated test fixture: stock hull, no weapons, no regeneration, never in a build list.
    target_dir = destination/"ship/vr_combat_target"
    target_dir.mkdir(parents=True, exist_ok=True)
    target_type = "hgn_ioncannonfrigate"
    carrier = project/"local/hw2ships/ship"/target_type
    for extension in ("hod", "events"):
        shutil.copyfile(carrier/(target_type+"."+extension), target_dir/("vr_combat_target."+extension))
    target = (carrier/(target_type+".ship")).read_text(encoding="utf-8-sig")
    target = re.sub(r'NewShipType.regentime=.*', 'NewShipType.regentime=0', target)
    target = re.sub(r'NewShipType.maxhealth=.*', 'NewShipType.maxhealth=20000', target)
    target = re.sub(r'^StartShipWeaponConfig.*\n', '', target, flags=re.MULTILINE)
    (target_dir/"vr_combat_target.ship").write_text(target, encoding="utf-8")
    print(f"Prepared {len(FLEET)} combat ships: {destination.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("local/testmod"))
    args = parser.parse_args()
    prepare(args.output)
