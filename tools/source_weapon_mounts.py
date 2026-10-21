"""Replace inherited add-on turrets with source-authored VR weapon mounts."""

import json
import math
import re
import struct
from pathlib import Path

from borrow_native_rig import chunks, form


# The source turret views are VFX-only; their visible geometry is in the hull.
# These weapons retain temporary HWRM projectile/damage definitions.
WEAPONS = {
    'nku_destroyer': ['Kus_DestroyerGun','Kus_DestroyerGun','Kus_DestroyerIon1','Kus_DestroyerIon2'],
    'nku_ballisticdestroyer': ['Hgn_DestroyerTorpedoLauncher'],
    'nku_barricadefrigate': [],
    'rad_destroyer': ['Vgr_FlechetteCannonDestroyer']*4+['Vgr_Laser']*2+['Vgr_HeavyFusionMissileLauncherWeak']*2,
    'rad_frigate': ['Tai_AssaultGun1','Tai_AssaultGun2','Tai_AssaultGun1','Tai_AssaultGun2','Tai_AssaultBomb','Tai_AssaultBomb'],
}


def read_hierarchy(chunk):
    count=struct.unpack_from('<i',chunk,12)[0]
    if count>=0:raise ValueError('Expected extended HWRM hierarchy')
    offset=16;nodes=[]
    for _ in range(-count):
        strings=[]
        for _ in range(2):
            size=struct.unpack_from('<I',chunk,offset)[0];offset+=4
            strings.append(chunk[offset:offset+size].decode('ascii'));offset+=size
        values=struct.unpack_from('<9f',chunk,offset);offset+=36
        nodes.append(dict(name=strings[0],parent=strings[1],values=list(values)))
    if offset!=len(chunk):raise ValueError('Unexpected trailing hierarchy data')
    return nodes


def write_hierarchy(nodes):
    payload=struct.pack('<i',-len(nodes))
    for node in nodes:
        for string in (node['name'],node['parent']):
            data=string.encode('ascii');payload+=struct.pack('<I',len(data))+data
        payload+=struct.pack('<9f',*node['values'])
    return form(b'HIER',payload)


def source_mounts(spec):
    definitions=json.loads(Path('local/recovered/definitions.json').read_text())
    turrets=definitions[spec['definition']]['_staticData']['<Turrets>k__BackingField']
    turrets=[t for t in turrets if t['InitialTurretState']==0]
    if len(turrets)!=len(WEAPONS[spec['id']]):raise ValueError('Source weapon mount count mismatch: '+spec['id'])
    scale=spec.get('scale',100)
    return [dict(name=f'Weapon_VR{i}',position=[-t['OffsetFromShipCenter']['x']*scale,
                t['OffsetFromShipCenter']['y']*scale,t['OffsetFromShipCenter']['z']*scale],
                direction=[-t['CenteredBarrelDirection']['x'],t['CenteredBarrelDirection']['y'],t['CenteredBarrelDirection']['z']],
                turret_type=t['TurretType'],weapon=weapon)
            for i,(t,weapon) in enumerate(zip(turrets,WEAPONS[spec['id']]))]


def apply(hod, spec, template, events, native_template):
    if spec['id'] not in WEAPONS:return template,events,None
    mounts=source_mounts(spec)
    binary=hod.read_bytes();output=[]
    for kind,chunk in chunks(binary):
        if kind==b'DTRM':
            entries=[]
            for subkind,subchunk in chunks(chunk,12):
                if subkind==b'HIER':
                    nodes=[n for n in read_hierarchy(subchunk) if not n['name'].startswith('Weapon_VR')]
                    for mount in mounts:
                        prefix=mount['name'];direction=mount['direction']
                        length=math.sqrt(sum(v*v for v in direction)) or 1
                        forward=[v/length for v in direction]
                        up=[-forward[0]*forward[1],1-forward[1]**2,-forward[2]*forward[1]]
                        up_length=math.sqrt(sum(v*v for v in up)) or 1
                        def node(name,parent,position):
                            return dict(name=name,parent=parent,values=[*position,0,0,0,0,0,0])
                        nodes += [node(prefix+'_Position','Root',mount['position']),
                                  node(prefix+'_Rest',prefix+'_Position',[v*10 for v in forward]),
                                  node(prefix+'_Direction',prefix+'_Position',[v/up_length*10 for v in up]),
                                  node(prefix+'_Muzzle',prefix+'_Position',[v*.1 for v in forward])]
                    subchunk=write_hierarchy(nodes)
                entries.append(subchunk)
            chunk=form(b'DTRM',b''.join(entries))
        output.append(chunk)
    hod.write_bytes(b''.join(output))
    # Remove foreign visible gun subsystems, while keeping engines and dock paths.
    template=re.sub(r'(?m)^[ \t]*(?:--[ \t]*)?StartShipWeaponConfig\([\s\S]*?\);[^\n]*','',template)
    template=re.sub(r'(?m)^[ \t]*StartShipHardPointConfig\([\s\S]*?\);',
                    lambda match:'' if ',"Weapon",' in match[0] else match[0],template)
    from prepare_test_mod import combat_events
    weapons=[m['weapon'] for m in mounts]
    events=combat_events(events,native_template,weapons)
    for i,mount in enumerate(mounts):
        template+=f'\nStartShipWeaponConfig(NewShipType,"{mount["weapon"]}","{mount["name"]}","VR_Fire{i}");'
        events=events.replace(f'Weapon_Gun{i}_Muzzle',mount['name']+'_Muzzle')
    report=dict(source_definition=spec['definition'],source_mounts=mounts,
                removed_foreign_weapon_subsystems=True,native_dock_and_repair_markers_preserved=True)
    return template,events,report
