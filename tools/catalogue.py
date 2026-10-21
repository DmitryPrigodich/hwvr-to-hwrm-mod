"""Additional demo hulls and temporary native gameplay archetypes."""

from pathlib import Path


def entry(identifier, title, root, archetype=None, definition=None, race=None):
    return dict(id=identifier, ru=title, root=root, archetype=archetype,
                definition=definition, race=race, buildable=bool(race and archetype))


ADDITIONAL = [
    entry("nku_assaultfrigate", "Штурмовой фрегат", "MESH_Kus_AssaultFrigate", "kus_assaultfrigate", "Ship_Hgn_AssaultFrigate", "novokushan"),
    entry("nku_barricadefrigate", "Баррикадный фрегат", "MESH_Hgn_BarricadeFrigate", "hgn_defensefieldfrigate", "Ship_Hgn_BarricadeFrigate", "novokushan"),
    entry("nku_destroyer", "Эсминец", "MESH_Kus_Destroyer", "kus_destroyer", "Ship_Hgn_Destroyer", "novokushan"),
    entry("nku_ballisticdestroyer", "Баллистический эсминец", "MESH_Hgn_BallisticDestroyer", "hgn_destroyer", "Ship_Hgn_BallisticDestroyer", "novokushan"),
    entry("nku_engineercorvette", "Инженерный корвет", "MESH_Hgn_EngineerCorvette", "kus_repaircorvette", "Ship_Hgn_EngineerCraft", "novokushan"),
    entry("nku_heavycorvette", "Тяжёлый корвет", "MESH_Kus_HeavyCorvette", "kus_heavycorvette", "Ship_Hgn_HeavyCorvette", "novokushan"),
    entry("nku_heavycruiser", "Тяжёлый крейсер", "MESH_Kus_HeavyCruiser", "kus_heavycruiser", "Ship_Hgn_HeavyCruiser", "novokushan"),
    entry("nku_miningplatform", "Добывающая платформа", "MESH_Hng_MiningPlatform_Pristine", "hgn_resourcecontroller", "Ship_Hgn_MiningPlatform", "novokushan"),
    entry("nku_mothership", "Материнский корабль", "MESH_Kus_Mothership", "kus_mothership", "Ship_Hgn_Mothership", "novokushan"),
    entry("nku_multiguncorvette", "Многопушечный корвет", "MESH_Kus_MultiGunCorvette", "kus_multiguncorvette", "Ship_Hgn_Multi-GunCorvette", "novokushan"),
    entry("nku_resourcecollector", "Сборщик ресурсов", "MESH_Kus_ResourceCollector", "kus_resourcecollector", "Ship_Hgn_ResourceCollector", "novokushan"),
    entry("nku_shipyard", "Верфь Новокушан", "MESH_Hgn_Shipyard", "hgn_shipyard", "Ship_Hgn_Shipyard", "novokushan"),
    entry("nku_mobilerefinery", "Мобильный переработчик", "MESH_Kus_MobileRefinery", "kus_resourcecontroller", "Ship_Kus_MobileRefinery", "novokushan"),
    entry("nku_carrier", "Носитель Новокушан", "MESH_Kus_Carrier", "kus_carrier", None, "novokushan"),
    entry("nku_supportfrigate", "Фрегат поддержки", "MESH_Kus_SupportFrigate", "kus_supportfrigate", None, "novokushan"),
    entry("nku_proximitysensor", "Датчик приближения", "MESH_Kus_ProximitySensor", "kus_proximitysensor", None, "novokushan"),
    entry("rad_battlecruiser", "Линейный крейсер", "MESH_Rad_Battlecruiser", "vgr_battlecruiser", "Ship_Rad_Battlecruiser", "radaa"),
    entry("rad_destroyer", "Эсминец Радаа", "MESH_Rad_Destroyer", "tai_destroyer", "Ship_Rad_Destroyer", "radaa"),
    entry("rad_frigate", "Штурмовой фрегат Радаа", "MESH_Rad_Frigate", "tai_assaultfrigate", "Ship_Rad_Frigate", "radaa"),
    entry("rad_gunplatform", "Орудийная платформа", "MESH_Rad_GunPlatform", "vgr_weaponplatform_gun", "Ship_Rad_GunPlatform", "radaa"),
    entry("rad_heavymissileplatform", "Тяжёлая ракетная платформа", "MESH_Rad_HeavyMissilePlatform", "vgr_weaponplatform_missile", "Ship_Rad_HeavyMissilePlatform", "radaa"),
    entry("rad_hyperspacegate", "Гиперврата", "MESH_Rad_HyperSpaceGate", "vgr_hyperspace_platform", "Ship_Rad_HyperSpaceGate", "radaa"),
    entry("rad_missilecorvette", "Многопушечный корвет Радаа", "MESH_Rad_MissileCorvette", "tai_multiguncorvette", "Ship_Rad_MissileCorvette", "radaa"),
    entry("rad_infiltrationfrigate", "Фрегат проникновения", "MESH_Rad_InfiltrationFrigate", "vgr_infiltratorfrigate", "Ship_Rad_MissileFrigate", "radaa"),
    entry("rad_mobilerefinery", "Переработчик Радаа", "MESH_Rad_Refinery", "vgr_resourcecontroller", "Ship_Rad_MobileRefinery", "radaa"),
    entry("rad_shieldemitter", "Мобильный командный центр / генератор щита", "MESH_Rad_MobileCommandCenter", "vgr_commandcorvette", "Ship_Rad_Shield Emitter", "radaa"),
    entry("rad_shipyard", "Верфь Радаа", "MESH_Rad_Shipyard", "vgr_shipyard", "Ship_Rad_Shipyard", "radaa"),
    entry("rad_tower", "Башня Радаа", "MESH_Rad_Tower", "vgr_weaponplatform_gun", "Ship_Rad_Tower", "radaa"),
    entry("rad_carrier", "Носитель Радаа", "MESH_Rad_Carrier", "vgr_carrier", None, "radaa"),
    entry("rad_commandcorvette", "Командный корвет", "MESH_Rad_CommandCorvette", "vgr_commandcorvette", None, "radaa"),
    entry("rad_heavymissilefrigate", "Тяжёлый ракетный фрегат", "MESH_Rad_HeavyMissileFrigate", "vgr_heavymissilefrigate", None, "radaa"),
    entry("vr_bentusi", "Корабль бентуси", "MESH_Ben_Exchange", definition="Ship_Ben_Bentusi"),
    entry("vr_shatterstation", "Shatter Station", "MESH_Rad_ShatterStation_Whole", definition="Ship_Rad_ShatterStation_Whole"),
    entry("vr_stationconsole", "Shatter Station: консоль", "MESH_Rad_ShatterStation_SectionConsole", definition="Ship_Rad_ShatterStation_SectionConsole"),
    entry("vr_stationwing", "Shatter Station: секция крыла", "MESH_Rad_ShatterStation_SectionWing", definition="Ship_Rad_ShatterStation_SectionWing"),
    entry("vr_destroyer_damaged", "Повреждённый эсминец Радаа", "MESH_Rad_Destroyer_Damaged", definition="Ship_Rad_Destroyer Damaged"),
]


def native_folder(archetype):
    return Path("local/hw1ships/ship" if archetype.startswith(("kus_", "tai_")) else "local/hw2ships/ship") / archetype
