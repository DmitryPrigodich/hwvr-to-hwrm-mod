"""Inspection categories and visual counterparts requested by the user."""


FACTIONS = [
    ('Новокушане', [
        ('Файтеры', [('nku_scout','kus_scout'),('nku_interceptor','kus_interceptor'),('nku_attackbomber','kus_attackbomber')]),
        ('Корветы', [('nku_heavycorvette','kus_heavycorvette'),('nku_multiguncorvette','kus_multiguncorvette'),('nku_engineercorvette',None)]),
        ('Фрегаты', [('nku_assaultfrigate','kus_assaultfrigate'),('nku_ioncannonfrigate','kus_ioncannonfrigate'),('nku_supportfrigate','kus_supportfrigate'),('nku_barricadefrigate',None),('vr_sm_shield_sphere',None)]),
        ('Капиталы', [('nku_carrier','kus_carrier'),('nku_heavycruiser','kus_heavycruiser'),('nku_destroyer','kus_destroyer'),('nku_ballisticdestroyer',None)]),
        ('Базы', [('nku_mothership','kus_mothership'),('vr_kus_mothership_door','vr_reference_kus_door'),('nku_shipyard','hgn_shipyard')]),
        ('Ресурсы', [('nku_resourcecollector','kus_resourcecollector'),('nku_mobilerefinery','kus_resourcecontroller')]),
        ('Прочее', [('nku_miningplatform',None),('nku_proximitysensor','kus_proximitysensor')]),
    ]),
    ('Радаа', [
        ('Файтеры', [('rad_assaultcraft','vgr_interceptor'),('rad_bomber','vgr_bomber'),('rad_lancefighter','vgr_lancefighter')]),
        ('Корветы', [('rad_lasercorvette','vgr_lasercorvette'),('rad_missilecorvette','tai_multiguncorvette'),('rad_commandcorvette','vgr_commandcorvette')]),
        ('Фрегаты', [('rad_frigate','tai_assaultfrigate'),('rad_infiltrationfrigate','vgr_infiltratorfrigate'),('rad_heavymissilefrigate','vgr_heavymissilefrigate')]),
        ('Капиталы', [('rad_carrier','vgr_carrier'),('rad_battlecruiser','vgr_battlecruiser'),('rad_destroyer','tai_destroyer'),('vr_destroyer_damaged','tai_destroyer')]),
        ('Базы', [('rad_shipyard','vgr_shipyard'),('rad_mobilerefinery','vgr_resourcecontroller')]),
        ('Платформы', [('rad_gunplatform','vgr_weaponplatform_gun'),('rad_heavymissileplatform','vgr_weaponplatform_missile'),('rad_hyperspacegate','vgr_hyperspace_platform')]),
        ('Прочее', [('rad_shieldemitter',None),('rad_tower',None)]),
    ]),
    ('NPC', [('Бентуси',[('vr_bentusi','ben_bentusiexchange')])]),
]


def all_categories(models):
    factions=[(name,[(title,list(entries)) for title,entries in groups]) for name,groups in FACTIONS]
    misc=[]
    for title,predicate in (
        ('Ракета',lambda m:m['id']=='vr_vgr_heavymissle'),
        ('Обломки',lambda m:any(s in m['id'] for s in ('rubbl','fragmentpanel','junkpanel','junksensors'))),
        ('Контейнер',lambda m:'container' in m['id']),
        ('Астероиды',lambda m:'asteroid' in m['id'] or 'radioactiverock' in m['id']),
        ('Станция',lambda m:'shatterstation' in m['id'] or m['id'] in ('vr_stationconsole','vr_stationwing')),
    ):
        misc.append((title,[(m['id'],None) for m in models.values() if predicate(m)]))
    factions.append(('MISC',misc))
    ordered=[identifier for _,groups in factions for _,entries in groups for identifier,_ in entries]
    if len(set(ordered))!=len(ordered):raise ValueError('An exhibit is assigned to two categories')
    if set(ordered)!=set(models):raise ValueError(f'Gallery coverage mismatch: {set(models)^set(ordered)}')
    return factions
