"""Prepare reviewable HWRM maps and conservative script bindings from Quest.

Writes only its campaign subtree, placements manifest and documentation.
Never launches, installs, packages, extracts audio or changes the mini-campaign.
"""
from __future__ import annotations
import collections
import json
import math
import re
from pathlib import Path

import write_quest_progression as q
from export_ship import rotate

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'campaign-export/data/leveldata/campaign/VastReachesFull'
MANIFEST = ROOT / 'campaign-export/manifests/placements.json'
NAME = 'VastReachesFull'
SCALE = 100.0
DIRECTORIES = {
    'T1': 'T01_Training', 'M1': 'M01_ProvingGrounds', 'M7': 'M07_AngelMoon',
    'M3': 'M03_GybbasRaid', 'M4': 'M04_LostDestroyer', 'M5': 'M05_HiigaraShipyard',
    'M6': 'M06_Weapon', 'M9': 'M09_Tenhauser', 'M10': 'M10_OuterReef',
    'M11': 'M11_WeaponArchitects', 'M8': 'M08_GybbasOffensive', 'M13': 'M13_ReturnToHiigara',
}
# Role mapping, not an assertion that matching silhouettes have matching weapons.
HULLS = {
    1: ('kus_mothership', 'native_hull'), 9: ('vgr_interceptor', 'native_role'),
    10: ('kus_interceptor', 'native_hull'), 11: ('vgr_battlecruiser', 'native_hull'),
    13: ('kus_attackbomber', 'native_hull'), 14: ('kus_heavycorvette', 'native_hull'),
    15: ('tai_assaultfrigate', 'native_hull'), 16: ('kus_carrier', 'cut_source_role'),
    18: ('kus_assaultfrigate', 'native_hull'), 19: ('kus_resourcecontroller', 'native_role'),
    20: ('kus_ioncannonfrigate', 'native_hull'), 21: ('kus_heavycruiser', 'native_hull'),
    22: ('kus_supportfrigate', 'cut_source_role'), 23: ('kus_scout', 'native_hull'),
    24: ('kus_multiguncorvette', 'native_hull'),
    25: ('vgr_resourcecontroller', 'partial_no_native_harvest'),
    26: ('kus_salvagecorvette', 'partial_engineer_capture_no_repair'),
    27: ('tai_destroyer', 'partial_damage_state'), 28: ('vgr_weaponplatform_gun', 'native_hull'),
    29: ('vgr_lancefighter', 'native_hull'), 30: ('kus_destroyer', 'native_hull'),
    31: ('vgr_lasercorvette', 'native_hull'), 32: ('tai_destroyer', 'native_hull'),
    33: ('vgr_commandcorvette', 'cut_source_role'), 34: ('vgr_heavymissilefrigate', 'cut_source_role'),
    35: ('vgr_bomber', 'native_hull'), 36: ('vgr_hyperspace_platform', 'native_role'),
    37: ('vgr_missilecorvette', 'native_missile_role_taiidan_silhouette_differs'),
    38: ('vgr_heavymissilefrigate', 'native_missile_role_not_capture'),
    39: ('vgr_weaponplatform_missile', 'native_hull'), 41: ('vgr_shipyard', 'native_hull'),
    43: ('hgn_shipyard', 'native_shipyard_role'), 44: ('ben_bentusiexchange', 'native_hull'),
    45: ('hgn_defensefieldfrigate', 'partial_shield_role'),
    46: ('kus_missiledestroyer', 'native_missile_role_unique_hull_differs'),
    49: ('tai_destroyer', 'partial_surrender_state'), 50: ('kus_resourcecollector', 'native_hull'),
    54: ('vgr_battlecruiser', 'partial_stationary_state'),
}
DEPENDENCIES = {
    8: 'VR mining platform: attachment points, silicon extraction and ram/tow adapter required.',
    40: 'Unused navigation-beacon definition; no arbitrary combat replacement.',
    42: 'Dummy ship: source helper only; no replacement hull.',
    47: 'VR shield-emitter hull plus capture/field linkage required.',
    48: 'VR Tower hull and internal-shield/end-state linkage required.',
    51: 'VR Shatter Station whole hull; do not replace with an unrelated native station.',
    52: 'VR Shatter Station section hull and per-section shield/damage linkage required.',
    53: 'VR Shatter Station console hull and finale linkage required.',
}
OWNER = {0: 3, 1: 0, 2: 2, 1024: 1, 2048: 1}
IDENTITY = dict(x=0.0, y=0.0, z=0.0, w=1.0)
PASSIVE_COMMANDS = {
    'LockControls', 'SetSensorsManagerDisplayMode', 'SpawnNotification', 'RemoveNotification',
    'CreateCustomVision', 'CreateHealthEvent', 'CreateLossEvent', 'ModifyHealth', 'EnableAttach',
    'SetCaptureRallyPoint', 'SetEntityVulnerability', 'ShowAlert', 'HideAlerts',
    'ShowControllerTags', 'HideControllerTags', 'ShowTutorialGesture', 'HideTutorialGesture',
    'PlaySuccessSound', 'PlayFailureSound', 'SetObjectiveCount',
}
SUPPORTED = {'OnSimReady', 'Sequence', 'WaitForSecondsUnit', 'PlayDialogue', 'AddObjective',
             'SpawnEntity', 'SetVariable', 'DisableBuildSystem', 'SetBuildByBuildList',
             'SetEntityActiveState'}


def read(path):
    return json.loads(path.read_text(encoding='utf8'))


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def lua(value):
    if value is None:
        return 'nil'
    if isinstance(value, bool):
        return '1' if value else '0'
    if isinstance(value, (int, float)):
        if not math.isfinite(value):
            raise ValueError('Non-finite coordinate')
        return str(round(value, 6))
    if isinstance(value, str):
        # Lua 4 accepts byte strings, not JSON \uXXXX escape sequences.
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return '{' + ','.join(lua(x) for x in value) + '}'
    return '{' + ','.join('[' + lua(str(k)) + ']=' + lua(v) for k, v in value.items()) + '}'


def ref(record):
    return record['source'] + ':' + str(record['path_id'])


def xyz(value):
    return [value.get(a, 0.0) for a in 'xyz']


def convert(point, origin):
    return [-(point[0] - origin[0]) * SCALE, (point[1] - origin[1]) * SCALE,
            (point[2] - origin[2]) * SCALE]


def multiply(a, b):
    ax, ay, az, aw = (a[k] for k in 'xyzw')
    bx, by, bz, bw = (b[k] for k in 'xyzw')
    return dict(zip('xyzw', [aw*bx+ax*bw+ay*bz-az*by, aw*by-ax*bz+ay*bw+az*bx,
                             aw*bz+ax*by-ay*bx+az*bw, aw*bw-ax*bx-ay*by-az*bz]))


def transform(record):
    raw = q.raw_file(record['source']).get(record['path_id'], record)
    go = raw if raw['class_name'] == 'GameObject' else q.pointer(raw['source'], raw['data'].get('m_GameObject', {}))
    if not go:
        return None
    for component in go['data'].get('m_Component', []):
        target = q.pointer(go['source'], component['component'])
        if target and target['class_name'] == 'Transform':
            return target
    return None


def world_point(record, point=(0.0, 0.0, 0.0)):
    tr, seen = transform(record), set()
    if tr is None:
        return record.get('world_position', xyz(record['data'].get('Position', {})))
    while tr:
        if ref(tr) in seen:
            raise ValueError('Cyclic Unity transform: ' + ref(tr))
        seen.add(ref(tr))
        d = tr['data']
        point = rotate([point[i] * d['m_LocalScale'][a] for i, a in enumerate('xyz')], d['m_LocalRotation'])
        point = [point[i] + d['m_LocalPosition'][a] for i, a in enumerate('xyz')]
        tr = q.pointer(tr['source'], d.get('m_Father', {}))
    return list(point)


def world_rotation(record):
    tr, value = transform(record), IDENTITY
    while tr:
        value = multiply(tr['data']['m_LocalRotation'], value)
        tr = q.pointer(tr['source'], tr['data'].get('m_Father', {}))
    return value


def active(record):
    raw = q.raw_file(record['source']).get(record['path_id'], record)
    if not raw['data'].get('m_Enabled', 1):
        return False
    tr = transform(raw)
    while tr:
        go = q.pointer(tr['source'], tr['data'].get('m_GameObject', {}))
        if go and not go['data'].get('m_IsActive', 1):
            return False
        tr = q.pointer(tr['source'], tr['data'].get('m_Father', {}))
    return True


def rotation_euler(value):
    # Mirror X: S R S corresponds to (x,-y,-z,w). HWRM Euler pose needs visual QA.
    x, y, z, w = value['x'], -value['y'], -value['z'], value['w']
    return [math.degrees(math.atan2(2*(w*x+y*z), 1-2*(x*x+y*y))),
            math.degrees(math.asin(max(-1, min(1, 2*(w*y-z*x))))),
            math.degrees(math.atan2(2*(w*z+x*y), 1-2*(y*y+z*z)))]


def animatic(scene_path):
    """Follow real PlayableDirector -> Timeline -> caption -> DialogueLine refs."""
    if not scene_path:
        return []
    built = read(ROOT/'local/quest-campaign/summary.json')['built_scenes']
    if scene_path not in built:
        return []
    scene_source = 'level'+str(built.index(scene_path))
    timelines = []
    for item in q.raw_file(scene_source).values():
        if item['class_name'] != 'PlayableDirector':
            continue
        target = q.pointer(item['source'],item['data'].get('m_PlayableAsset',{}))
        if target and target['class_name'].endswith('.TimelineAsset') and target['name'].startswith('M'):
            timelines.append(target)
    clips, visited = [], set()
    def visit(track):
        if not track or ref(track) in visited:
            return
        visited.add(ref(track))
        data=track['data']
        if data.get('m_Muted'):
            return
        if track['class_name']=='Hercules.AnimaticCaptionTrack':
            for clip in data.get('m_Clips',[]):
                asset=q.pointer(track['source'],clip['m_Asset'])
                line=q.pointer(asset['source'],asset['data'].get('Data',{}).get('DialogueLine',{})) if asset else None
                if line:
                    clips.append(dict(key=line['data']['_textKey'],start=clip['m_Start'],duration=clip['m_Duration'],
                                      source_track=ref(track),source_dialogue=ref(line),source_asset=ref(asset)))
        for p in data.get('m_Tracks',[])+data.get('m_Children',[]):
            visit(q.pointer(track['source'],p))
    for timeline in timelines:
        visit(timeline)
    return sorted(clips,key=lambda clip:clip['start'])


def native_path(hull):
    for root in ['hw1ships', 'hw2ships', 'hwrm-base']:
        path = ROOT / 'local' / root / 'ship' / hull / (hull + '.ship')
        if path.is_file():
            return path
    raise FileNotFoundError('Missing native hull: ' + hull)


def unbox(value):
    return value.get('$content') if isinstance(value, dict) and '$content' in value else value


def expression(graph, node, port, seen=None):
    """Only constants/variables; no speculative execution of Unity methods."""
    nodes, value_in, _, _ = q.node_maps(graph)
    seen = set() if seen is None else seen
    for key, parent in value_in.get(node.get('$id'), []):
        if key != port or parent in seen:
            continue
        target = nodes[parent]
        kind = target['$type'].split('.')[-1]
        if kind == 'Literal':
            return dict(kind='literal', value=unbox(target.get('value')))
        if kind == 'GetVariable':
            return dict(kind='variable', name=unbox(target.get('defaultValues', {}).get('name')), scope=target.get('kind'))
        return dict(kind='unresolved', source_node=parent, source_kind=kind)
    value = node.get('defaultValues', {}).get(port)
    if isinstance(value, dict) and value.get('$type') == 'UnityEngine.Object':
        index = value.get('$content')
        return dict(kind='object', reference=graph['object_references'][index] if index is not None else None)
    return dict(kind='literal', value=unbox(value))


def graph_bindings(info, groups_by_ref):
    graph_list, runtime, roots, unsupported = [], {}, [], collections.Counter()
    for context_index, (label, graph) in enumerate(q.contexts(info['graph'], info['mission']['id'])):
        prefix = 'g' + str(context_index) + ':'
        nodes, _, incoming, outgoing = q.node_maps(graph)
        context = dict(label=label, source=graph['source'], nodes=[], edges=graph['edges'])
        for node in graph['nodes']:
            ident = node.get('$id')
            if not ident:
                continue
            kind = node['$type'].split('.')[-1]
            connected = bool(incoming.get(ident) or outgoing.get(ident))
            edges = [dict(port=e['sourceKey'], target=prefix+e['destinationUnit']['$ref'])
                     for e in graph['edges'] if e['$type'].endswith('.ControlConnection') and e['sourceUnit']['$ref'] == ident]
            if kind == 'Sequence':
                edges.sort(key=lambda e: int(e['port']) if str(e['port']).isdigit() else str(e['port']))
            args = {k: unbox(v) for k, v in node.get('defaultValues', {}).items()}
            status = 'adapter' if kind in SUPPORTED else ('recorded_command_pending' if kind in PASSIVE_COMMANDS else 'missing_handler')
            entry = dict(id=prefix+ident, source_graph=label, source_id=ident, kind=kind, status=status,
                         connected=connected, source_args=args, resolved_objects=node.get('resolved_objects', {}),
                         editor_group=q.group_label(graph, node), previous=q.nearby_context(graph, node) if connected else '',
                         outgoing=edges, expressions={key: expression(graph, node, key) for key in set(args) | {'input', '_enable', 'seconds', 'Tag', 'ActiveState'}})
            entry['original_node']=node
            if kind == 'PlayDialogue':
                detail = q.dialogue_ref(graph, node)
                entry['text_key'] = detail.get('text_key') if detail else None
            if kind == 'AddObjective':
                detail = next((r for r in node.get('resolved_objects', {}).values() if r and r.get('text_key')), None)
                if not detail:
                    value = node.get('defaultValues', {}).get('ObjectiveDefinition', {})
                    index = unbox(value)
                    if index is not None:
                        pointer = graph['object_references'][index]
                        raw = q.raw_file(pointer['source'])[pointer['path_id']]
                        detail = dict(text_key=raw['data']['StaticData']['LocalizationKey'])
                entry['text_key'] = detail.get('text_key') if detail else None
            if kind == 'SpawnEntity':
                targets = q.spawn_targets(graph, info['scene'], node)
                entry['spawners'] = [dict(alias=alias, source_ref=ref(target), group=groups_by_ref.get(ref(target))) for alias, target in targets]
            if kind == 'OnSimReady' and context_index == 0 and connected:
                roots.append(prefix+ident)
            context['nodes'].append(entry)
            runtime[entry['id']] = {k: v for k, v in entry.items() if k in ['kind','status','outgoing','expressions','text_key','spawners']}
            if connected and status != 'adapter':
                unsupported[kind] += 1
        graph_list.append(context)
    return graph_list, runtime, roots, dict(unsupported)


RUNTIME = r'''-- Conservative Lua 4-compatible inspection runtime; no automatic victory.
dofilepath("data:scripts/SCAR/SCAR_Util.lua")
dofilepath("data:scripts/VRE_Text.lua")
VREX_Fibers={}
VREX_Time=0
VREX_Objectives={}
VREX_Variables={}
VREX_ActiveRoutes={}
VREX_Spawned={}
VREX_Pending={}

function VREX_PendingHandler(key,kind)
    if key==nil then key="<unresolved>" end
    if VREX_Pending[key]==nil then
        print("VRE_EXPORT: PENDING "..key.." "..kind)
        VREX_Pending[key]=1
    end
end

function VREX_GetText(key)
    if key==nil then return "[source text missing]" end
    if VRE_Text[key]~=nil then return VRE_Text[key] end
    return key
end

function VREX_Line(key)
    local duration=12
    if VRE_Duration~=nil and VRE_Duration[key]~=nil then duration=VRE_Duration[key] end
    if VRE_AudioDuration~=nil and VRE_AudioDuration[key]~=nil then duration=VRE_AudioDuration[key] end
    if VRE_PlayLine~=nil then VRE_PlayLine(key)
    else Subtitle_Message(VREX_GetText(key),duration) end
    return duration
end

function VREX_Expr(expr)
    if expr==nil then return nil end
    if expr.kind=="literal" then return expr.value end
    if expr.kind=="variable" then return VREX_Variables[expr.name] end
    return nil
end

function VREX_ApplyBuild(enabled)
    VREX_BuildEnabled=enabled
    for i=1,getn(VREX_Config.all_builds) do Player_RestrictBuildOption(0,VREX_Config.all_builds[i]) end
    if enabled==1 then
        for i=1,getn(VREX_Config.allowed_builds) do Player_UnrestrictBuildOption(0,VREX_Config.allowed_builds[i]) end
    end
end

function VREX_SetState(group,state)
    local enabled=1
    if state=="Disabled" or state==1 then enabled=0 end
    SobGroup_AbilityActivate(group,AB_Move,enabled)
    SobGroup_AbilityActivate(group,AB_Attack,enabled)
end

function VREX_SpawnGroup(key)
    local g=VREX_Config.groups[key]
    if g==nil then
        local p=VREX_Config.patrols[key]
        if p~=nil then return VREX_SpawnPatrol(key) end
        VREX_PendingHandler(key,"unresolved spawner") return 0
    end
    if VREX_Spawned[key]==1 then
        VREX_PendingHandler(key,"repeat spawn requires a new instance, not revival") return 0
    end
    if getn(g.units)==0 then VREX_PendingHandler(key,"required unique hull not connected") return 0 end
    for i=1,getn(g.units) do
        local unit=g.units[i]
        if g.initial~=1 then SobGroup_Spawn(unit.name,unit.volume) end
        if unit.active_state==1 then VREX_SetState(unit.name,"Disabled") end
        if unit.stationary==1 then SobGroup_SetMaxSpeed(unit.name,0) end
        if unit.source_vulnerability==2 then SobGroup_SetInvulnerability(unit.name,1) end
        if unit.source_vulnerability==1 then VREX_PendingHandler(unit.name,"disableable damage threshold pending") end
    end
    VREX_Spawned[key]=1
    print("VRE_EXPORT: spawned "..key.." requested_hulls="..getn(g.units).." engine_count="..SobGroup_Count(g.sob))
    return 1
end

function VREX_MoveRoute(key,route)
    local g=VREX_Config.groups[key]
    local points=VREX_Config.routes[route]
    if g==nil or points==nil or getn(points)==0 then return 0 end
    VREX_ActiveRoutes[key]={route=route,index=1}
    SobGroup_Move(g.owner,g.sob,points[1])
    return 1
end

function VREX_SpawnPatrol(key)
    local p=VREX_Config.patrols[key]
    if p==nil or getn(p.variants)==0 then VREX_PendingHandler(key,"empty patrol") return 0 end
    local chosen=p.variants[random(1,getn(p.variants))]
    if VREX_SpawnGroup(chosen)~=1 then return 0 end
    if getn(p.routes)>0 then VREX_MoveRoute(chosen,p.routes[random(1,getn(p.routes))]) end
    return 1
end

function VREX_StartNode(key)
    tinsert(VREX_Fibers,{stack={key},wake=VREX_Time})
end

-- Call only from a subsequently implemented real condition adapter.
-- This function is not bound to a debug key, timer victory or fake condition.
function VREX_SourceEvent(key)
    local node=VREX_Nodes[key]
    if node==nil then VREX_PendingHandler(key,"unknown source event") return end
    for i=1,getn(node.outgoing) do VREX_StartNode(node.outgoing[i].target) end
end

function VREX_Node(fiber,key)
    local node=VREX_Nodes[key]
    if node==nil then VREX_PendingHandler(key,"missing source node") return 0 end
    local kind=node.kind
    local proceed=1
    if kind=="PlayDialogue" then fiber.wake=VREX_Time+VREX_Line(node.text_key)
    elseif kind=="WaitForSecondsUnit" then
        local seconds=VREX_Expr(node.expressions.seconds)
        if type(seconds)~="number" then VREX_PendingHandler(key,"unresolved delay") return 0 end
        fiber.wake=VREX_Time+seconds
    elseif kind=="AddObjective" then
        if node.text_key==nil then VREX_PendingHandler(key,"unresolved objective") return 0 end
        if VREX_Objectives[node.text_key]==nil then
            VREX_Objectives[node.text_key]=Objective_Add(VREX_GetText(node.text_key),OT_Primary)
        end
    elseif kind=="SpawnEntity" then
        if node.spawners==nil or getn(node.spawners)==0 then VREX_PendingHandler(key,"unresolved SpawnEntity") return 0 end
        for i=1,getn(node.spawners) do
            if VREX_SpawnGroup(node.spawners[i].group)~=1 then proceed=0 end
        end
    elseif kind=="SetVariable" then
        local name=VREX_Expr(node.expressions.name)
        if name~=nil then VREX_Variables[name]=VREX_Expr(node.expressions.input) end
        VREX_PendingHandler(key,"variable scope/value requires review")
    elseif kind=="DisableBuildSystem" then VREX_ApplyBuild(0)
    elseif kind=="SetBuildByBuildList" then
        local value=VREX_Expr(node.expressions._enable)
        if value==nil then VREX_PendingHandler(key,"unresolved build enable") return 0 end
        VREX_ApplyBuild(value)
    elseif kind=="SetEntityActiveState" then
        local tag=VREX_Expr(node.expressions.Tag)
        local state=VREX_Expr(node.expressions.ActiveState)
        local groups=VREX_Config.tags[tag]
        if groups~=nil then
            for i=1,getn(groups) do VREX_SetState(groups[i],state) end
        end
        VREX_PendingHandler(key,"active-state adapter covers Move/Attack only")
    elseif node.status=="recorded_command_pending" then
        -- Original instant command is kept in VREX_SourceBindings.json.
        -- Event registration/VR visuals are pending, never presumed satisfied.
        VREX_PendingHandler(key,kind)
    elseif kind~="OnSimReady" and kind~="Sequence" then
        VREX_PendingHandler(key,kind.." blocks this branch; real handler required")
        return 0
    end
    if proceed~=1 then return 0 end
    for i=getn(node.outgoing),1,-1 do tinsert(fiber.stack,node.outgoing[i].target) end
    return 1
end

function VREX_Tick()
    VREX_Time=VREX_Time+1
    if VREX_Started~=1 then
        while VREX_IntroIndex<=getn(VREX_Config.intro) and VREX_Config.intro[VREX_IntroIndex].start<=VREX_Time do
            VREX_Line(VREX_Config.intro[VREX_IntroIndex].key)
            VREX_IntroIndex=VREX_IntroIndex+1
        end
        if VREX_Time<VREX_IntroEnd then return end
        VREX_StartGameplay()
    end
    for i=1,getn(VREX_Fibers) do
        local fiber=VREX_Fibers[i]
        local budget=128
        while fiber.wake<=VREX_Time and getn(fiber.stack)>0 and budget>0 do
            local key=tremove(fiber.stack)
            if VREX_Node(fiber,key)~=1 then fiber.stack={} end
            budget=budget-1
        end
    end
    for i=1,getn(VREX_Config.group_keys) do
        local key=VREX_Config.group_keys[i]
        local active=VREX_ActiveRoutes[key]
        if active~=nil then
            local g=VREX_Config.groups[key]
            local route=VREX_Config.routes[active.route]
            if SobGroup_IsInVolume(g.sob,route[active.index])==1 then
                active.index=active.index+1
                if active.index>getn(route) then active.index=1 end
                SobGroup_Move(g.owner,g.sob,route[active.index])
            end
        end
    end
end

function VREX_StartGameplay()
    VREX_Started=1
    VREX_ApplyBuild(1)
    for i=1,getn(VREX_Config.group_keys) do
        local g=VREX_Config.groups[VREX_Config.group_keys[i]]
        if g.initial==1 then
            for j=1,getn(g.units) do
                local unit=g.units[j]
                VREX_SetState(unit.name,unit.active_state)
                local invulnerable=0
                if unit.source_vulnerability==2 then invulnerable=1 end
                SobGroup_SetInvulnerability(unit.name,invulnerable)
                if unit.stationary==1 then SobGroup_SetMaxSpeed(unit.name,0) end
            end
        end
    end
    for i=1,getn(VREX_Config.initial_patrols) do VREX_SpawnPatrol(VREX_Config.initial_patrols[i]) end
    for i=1,getn(VREX_Start) do VREX_StartNode(VREX_Start[i]) end
end

function VREX_Init()
    for i=1,3 do CPU_Enable(i,0) end
    SetAlliance(0,2) SetAlliance(2,0)
    SetAlliance(0,3) SetAlliance(3,0)
    SetAlliance(1,3) SetAlliance(3,1)
    SetAlliance(2,3) SetAlliance(3,2)
    for i=1,getn(VREX_Config.all_research) do Player_RestrictResearchOption(0,VREX_Config.all_research[i]) end
    VREX_ApplyBuild(1)
    for i=1,getn(VREX_Config.group_keys) do
        local key=VREX_Config.group_keys[i]
        if VREX_Config.groups[key].initial==1 then VREX_SpawnGroup(key) end
    end
    VREX_IntroIndex=1
    VREX_IntroEnd=0
    VREX_Started=0
    for i=1,getn(VREX_Config.intro) do
        local clip=VREX_Config.intro[i]
        if clip.start+clip.duration>VREX_IntroEnd then VREX_IntroEnd=clip.start+clip.duration end
    end
    if getn(VREX_Config.intro)==0 then VREX_StartGameplay()
    else
        VREX_ApplyBuild(0)
        for i=1,getn(VREX_Config.group_keys) do
            local g=VREX_Config.groups[VREX_Config.group_keys[i]]
            if g.initial==1 then
                for j=1,getn(g.units) do
                    VREX_SetState(g.units[j].name,"Disabled")
                    SobGroup_SetInvulnerability(g.units[j].name,1)
                end
            end
        end
    end
    Camera_Interpolate("here","VREX_HomeCamera",0)
    Rule_AddInterval("VREX_Tick",1)
    print("VRE_EXPORT: review scaffold "..VREX_Config.mission.."; no automatic objective completion or victory")
end
'''


def prepare_mission(mission, locale):
    info = q.mission_info(mission)
    scene = info['scene']
    code = mission['id'].removeprefix('Mission_')
    directory = DIRECTORIES[code]
    folder = OUT / directory
    folder.mkdir(parents=True, exist_ok=True)
    mother = next(p for p in scene['placements'] if p['class_name'].endswith('SquadronSpawner') and p['data'].get('Type') == 1)
    origin = world_point(mother)
    record = dict(mission=mission['id'], directory=directory, scene=mission['scene_file'],
                  source_definition=ref(mission), source_quest_order=mission['order'],
                  carryover=bool(mission['carryover']), snapshot='DefaultGroups + AdditionalGroups; previous-save carryover not emulated.',
                  origin_unity=origin, scale=SCALE, groups=[], patrols=[], resources=[], areas=[], routes=[], dependencies=[],
                  source_starting_ru=mission['starting_ru'], source_fleet_cap_squadrons=mission['fleet_cap'])
    record['intro']=[] if code=='M1' else animatic(mission['intro_scene'])
    record['intro_dedup']='Shared M1 intro is assigned only to T1.' if code=='M1' else None
    record['outro']=animatic(info['raw']['data'].get('_outroScene',{}).get('_path',''))
    record['outro_status']='Preserved for a future genuine victory handler; never auto-played as a fake win.'
    groups, by_ref, patrols, routes, tag_groups, all_positions = {}, {}, {}, {}, collections.defaultdict(list), []
    lines = ['-- Quest review export: deferred units use native sleeping/hyperspace flag.', 'function DetermChunk()',
             '    createSOBGroup("VREX_Player")', '    createSOBGroup("VREX_Enemy")',
             '    createSOBGroup("VREX_FriendlyNPC")', '    createSOBGroup("VREX_Neutral")',
             '    createSOBGroup("VREX_Mothership")']

    def add_group(source, key, policy, position=None, rotation=None):
        d = source['data'].get('_data', source['data'])
        position = world_point(source) if position is None else position
        rotation = world_rotation(source) if rotation is None else rotation
        owner = OWNER.get(d.get('TeamId', 0), 3)
        name = 'VREX_' + key
        initial = int(policy in ('scene_auto', 'default_loadout', 'additional_loadout') and active(source))
        result = dict(source_ref=ref(source), source_name=source.get('name', ''), key=key, sob=name, policy=policy,
                      initial=initial, owner=owner, source_team=d.get('TeamId'), active_in_hierarchy=active(source),
                      source_hyperspace=d.get('IsHyperspaceWarp', 0), tags=d.get('Tags', []),
                      position_unity=position, position=convert(position, origin), rotation_unity=rotation, units=[], squadrons=[])
        lines.append('    createSOBGroup(' + lua(name) + ')')
        members = d.get('Members', [dict(Type=d['Type'])] if 'Type' in d else [])
        if d.get('HasUniqueMember') and d.get('UniqueMemberInit', {}).get('Type'):
            members = members + [dict(Type=d['UniqueMemberInit']['Type'])]
        for index, member in enumerate(members, 1):
            ship_type = member['Type']
            ship = q.SHIPS[ship_type]
            count = q.squadron_count(ship_type)
            offset = rotate(xyz(member.get('Offset', {})), rotation)
            center = [position[i] + offset[i] for i in range(3)]
            hull, status = HULLS.get(ship_type, (None, 'missing_unique_hull'))
            squadron = dict(type=ship_type, definition=ship['name'], source_ref=ref(ship), source_count=count,
                            native_hull=hull, mapping=status, center=convert(center, origin), units=[])
            result['squadrons'].append(squadron)
            if hull is None:
                dep = dict(group=key, type=ship_type, definition=ship['name'], requested_hulls=count,
                           reason=DEPENDENCIES.get(ship_type, 'No approved native role mapping.'), position=convert(center, origin))
                record['dependencies'].append(dep)
                lines.append('    addSphere(' + lua(name+'_Missing_'+str(index)) + ',' + lua(dep['position']) + ',250)')
                continue
            native_path(hull)
            ship_data = ship['data']['_staticData']
            spacing = max(20, ship_data.get('<BoundingSphereRadius>k__BackingField', 0.5) * SCALE * 2.2)
            for body in range(count):
                # Explicit bodies per logical VR squadron; never infer from buildBatch.
                local_offset = [(body-(count-1)/2) * spacing/SCALE, 0, 0]
                spread = rotate(local_offset, rotation)
                point = convert([center[i]+spread[i] for i in range(3)], origin)
                unit_name = name+'_S'+str(index)+'_H'+str(body+1)
                unit = dict(name=unit_name, hull=hull, position=point, rotation=rotation_euler(rotation),
                            owner=owner, volume=unit_name+'_Spawn', active_state=d.get('ActiveState', 0),
                            source_vulnerability=d.get('Vulnerability', 0), stationary=int(ship_type == 54))
                result['units'].append(unit)
                squadron['units'].append(unit_name)
                all_positions.append(point)
                lines.append('    addSquadron('+','.join([lua(unit_name),lua(hull),lua(point),str(owner),lua(unit['rotation']),'1',str(1-initial)])+')')
                lines.append('    addSphere('+lua(unit['volume'])+','+lua(point)+',1)')
                lines.append('    createSOBGroup('+lua(unit_name)+')')
                lines.append('    addToSOBGroup('+lua(unit_name)+','+lua(unit_name)+')')
                lines.append('    addToSOBGroup('+lua(unit_name)+','+lua(name)+')')
                collection = {0:'VREX_Player',1:'VREX_Enemy',2:'VREX_FriendlyNPC',3:'VREX_Neutral'}[owner]
                lines.append('    addToSOBGroup('+lua(unit_name)+','+lua(collection)+')')
                if ship_type == 1 and owner == 0:
                    lines.append('    addToSOBGroup('+lua(unit_name)+',"VREX_Mothership")')
        for tag in result['tags']:
            tag_groups[tag].append(name)
        groups[key] = result
        record['groups'].append(result)
        return key

    # Scene spawners are distinct from loadout-prefab references, even when types match.
    for source in scene['placements']:
        if not source['class_name'].endswith(('GroupSpawner','SquadronSpawner')):
            continue
        key = 'Scene_'+str(source['path_id'])
        add_group(source, key, 'scene_auto' if source.get('auto_spawn') else 'script_deferred')
        by_ref[ref(source)] = key
    spawn_slots = [p for row in scene['loadout_positions'] for p in row['spawn_positions']]
    slot_index = 0
    for field in ['default_groups','additional_groups']:
        for source in mission[field]:
            if slot_index >= len(spawn_slots):
                raise ValueError('Insufficient source LoadoutSpawner slots: '+mission['id'])
            slot = spawn_slots[slot_index]
            tr = q.pointer(mission['scene_file'], slot['reference'])
            add_group(source, 'Loadout_'+str(slot_index+1), 'default_loadout' if field=='default_groups' else 'additional_loadout',
                      position=slot['world_position'], rotation=world_rotation(tr))
            slot_index += 1
    for source in scene['routes']:
        if not source['class_name'].endswith('.Route'):
            continue
        key = 'Route_'+str(source['path_id'])
        points = [convert(world_point(source, xyz(p)), origin) for p in source['data'].get('_localWaypoints', [])]
        route_names = []
        for index, point in enumerate(points, 1):
            name = 'VREX_'+key+'_'+str(index)
            lines.append('    addSphere('+lua(name)+','+lua(point)+',150)')
            route_names.append(name)
            all_positions.append(point)
        routes[key] = route_names
        record['routes'].append(dict(key=key, source_ref=ref(source), points=points, volumes=route_names))
    initial_patrols = []
    for source in scene['routes']:
        if not source['class_name'].endswith('.PatrolManager'):
            continue
        key = 'Patrol_'+str(source['path_id'])
        by_ref[ref(source)] = key
        data = source['data']
        variants = []
        poses = data.get('_spawnPoints') or [dict(position=dict(x=0,y=0,z=0), rotation=IDENTITY)]
        for gi, pointer in enumerate(data.get('_groups', []),1):
            group = q.pointer(source['source'],pointer)
            if not group:
                continue
            for pi, pose in enumerate(poses,1):
                variants.append(add_group(group,key+'_V'+str(gi)+'_P'+str(pi),'patrol_variant',
                                          position=world_point(source,xyz(pose['position'])),
                                          rotation=multiply(world_rotation(source),pose['rotation'])))
        route_keys = ['Route_'+str(q.pointer(source['source'],p)['path_id']) for p in data.get('_routes',[]) if q.pointer(source['source'],p)]
        patrols[key] = dict(variants=variants, routes=route_keys)
        record['patrols'].append(dict(key=key, source_ref=ref(source), initial=bool(data.get('_autoSpawn') and active(source)),
                                     variants=variants,routes=route_keys,repeat='One-shot preparation; free-route pool and repeats pending.'))
        if data.get('_autoSpawn') and active(source):
            initial_patrols.append(key)
    prop_defs = {r['data']['_staticData']['<Type>k__BackingField']:r for r in q.records_of_type('Hercules.Designer.PropDefinition')}
    for source in scene['placements']:
        if not source['class_name'].endswith('PropSpawner'):
            continue
        d = source['data']['_data']
        definition = prop_defs.get(d['Type'])
        point = convert(world_point(source), origin)
        all_positions.append(point)
        is_asteroid = bool(definition and definition['name'].startswith('Prop_Asteroid_'))
        auto = bool(source['data'].get('_autoSpawn') and active(source))
        ru = d.get('ContainedRu',0)
        item = dict(source_ref=ref(source), definition=definition['name'] if definition else None,
                    position=point, source_ru=ru, source_scale=d.get('Scale'), resource_tag=d.get('ResourceGroupTag'),
                    initial=auto, native_hull=('Asteroid_4' if ru>0 else 'Asteroid_1') if is_asteroid else None)
        if is_asteroid and auto:
            item['resource_multiplier'] = ru/18000 if ru>0 else 0
            lines.append('    addAsteroid('+lua(item['native_hull'])+','+lua(point)+','+lua(item['resource_multiplier'])+',0,0,0,0)')
        else:
            item['pending'] = 'Deferred resource appearance or non-asteroid prop requires adapter.'
        record['resources'].append(item)
    for source in scene['areas']:
        d = source['data']
        radius = d.get('_radius', d.get('Radius',0)) * SCALE
        if source['class_name'].endswith('VisionSphereInitializer'):
            center=world_point(source)
            axis=world_point(source,(1,0,0))
            radius=0.5*math.sqrt(sum((axis[i]-center[i])**2 for i in range(3)))*SCALE
        point = convert(world_point(source), origin)
        key = 'VREX_Area_'+str(source['path_id'])
        if radius>0:
            lines.append('    addSphere('+lua(key)+','+lua(point)+','+lua(radius)+')')
        all_positions.append(point)
        record['areas'].append(dict(name=key, source_ref=ref(source), class_name=source['class_name'], position=point,
                                    radius=radius, source_settings=d, state='Geometry only; detection/vision event adapter pending.'))
    max_half = [max([abs(p[i]) for p in all_positions]+[10000])+5000 for i in range(3)]
    lines += ['    addCamera("VREX_HomeCamera",{0,0,0},{3500,2000,-4500})',
              '    setWorldBoundsInner({0,0,0},'+lua(max_half)+')','end','function NonDetermChunk()',
              '    loadBackground("m01")','    setSensorsManagerCameraDistances(100,150000)','end',
              'levelDesc='+lua('$'+str(locale[info['raw']['data']['_missionNameKey']]['id'])),
              'maxPlayers=4','player={}',
              'player[0]={id=0,name="",resources='+str(mission['starting_ru'])+',raceName="Kushan",startPos=0}',
              'player[1]={id=1,name="",resources=0,raceName="Vaygr",startPos=0}',
              'player[2]={id=2,name="",resources=0,raceName="Hiigaran",startPos=0}',
              'player[3]={id=3,name="",resources=0,raceName="Kushan",startPos=0}']
    (folder/(directory+'.level')).write_text('\n'.join(lines)+'\n',encoding='utf8')
    bindings, runtime_nodes, starts, unsupported = graph_bindings(info,by_ref)
    record['unsupported_connected_nodes'] = unsupported
    record['source_bindings'] = str((folder/'VREX_SourceBindings.json').relative_to(ROOT)).replace('\\','/')
    record['startup_nodes'] = starts
    allowed = sorted({HULLS[b['data']['_shipType']][0] for b in info['available'] if b['data']['_shipType'] in HULLS})
    all_builds = sorted(set(re.findall(r'ThingToBuild\s*=\s*"([^"]+)"',(ROOT/'local/hwrm-base/scripts/races/kushan/scripts/def_build.lua').read_text())))
    all_research = sorted({name for p in (ROOT/'local/hwrm-base/scripts/races/kushan/scripts/research').glob('*.lua')
                           for name in re.findall(r'\bName\s*=\s*"([^"]+)"',p.read_text())})
    record['build'] = dict(source_mode=info['mode'], available=[dict(name=b['name'], source_ref=ref(b), data=b['data']) for b in info['available']],
                           allowed_native=allowed, pending='Whitelist is applied; non-Kushan hulls/custom builders and native prerequisite bypass are not invented.')
    record['build']['source_controller']=info['controller']
    record['build']['source_listed']=[dict(name=b['name'],source_ref=ref(b),data=b['data']) for b in info['listed']]
    config = dict(mission=mission['id'], groups={k:{f:v for f,v in g.items() if f in ['sob','owner','initial','units']} for k,g in groups.items()},
                  group_keys=list(groups),patrols=patrols,initial_patrols=initial_patrols,routes=routes,tags=dict(tag_groups),
                  all_builds=all_builds,all_research=all_research,allowed_builds=allowed)
    config['intro']=record['intro']
    config['outro']=record['outro']
    (folder/'VREX_Setup.lua').write_text('VREX_Config='+lua(config)+'\nVREX_Nodes='+lua(runtime_nodes)+'\nVREX_Start='+lua(starts)+'\n',encoding='utf8')
    save(folder/'VREX_SourceBindings.json',dict(source_mission=mission, source_graphs=bindings,
                                              connected_missing=unsupported, notes='No automatic completion, end-screen, capture, lesson or objective-condition adapter.'))
    loader = 'dofilepath("data:leveldata/campaign/'+NAME+'/'+directory+'/VREX_Setup.lua")\n'
    loader += 'dofilepath("data:leveldata/campaign/'+NAME+'/VREX_Common.lua")\n'
    if (ROOT/'campaign-export/data/scripts/VRE_Dialogue.lua').is_file():
        loader += 'dofilepath("data:scripts/VRE_Dialogue.lua")\n'
    loader += 'function OnInit()\n    VREX_Init()\nend\n'
    (folder/(directory+'.lua')).write_text(loader,encoding='ascii')
    return record


def main():
    locale = read(ROOT/'campaign-export/manifests/localization.json')
    missions = sorted([m for m in q.MISSIONS if m['category']=='_tutorialMissions'],key=lambda m:m['order'])
    missions += sorted([m for m in q.MISSIONS if m['category']=='_campaignMissions'],key=lambda m:m['order'])
    assert len(missions)==12 and missions[0]['id']=='Mission_T1'
    OUT.mkdir(parents=True,exist_ok=True)
    records = [prepare_mission(m,locale) for m in missions]
    (OUT/'VREX_Common.lua').write_text(RUNTIME,encoding='ascii')
    campaign = ['displayName="${}"'.format(locale['export_campaign']['id']), 'contentType=0',
                'contentName="'+NAME+'"','contentOrdered=0',
                'contentChooseText="${}"'.format(locale['export_choose']['id']),
                'contentRules="SinglePlayer"','ExtFilter="campaign_ascension,campaign_gbx,campaign_gbx_ascension"','Mission={}']
    for index, record in enumerate(records,1):
        code = record['mission'].removeprefix('Mission_')
        mission_raw=q.raw_file(missions[index-1]['source'])[missions[index-1]['path_id']]['data']
        title, description = locale[mission_raw['_missionNameKey']]['id'],locale[mission_raw['_missionDescriptionKey']]['id']
        d = record['directory']
        campaign.append('Mission['+str(index)+']={postload=function() end,directory='+lua(d)+',level='+lua(d+'.level')+
                        ',postlevel=function() postLevelComplete() end,displayName='+lua('$'+str(title))+',description='+lua('$'+str(description))+'}')
    (OUT.parent/(NAME+'.campaign')).write_text('\n'.join(campaign)+'\n',encoding='ascii')
    manifest = dict(identity='VastReachesFull-Quest-inspection-export', scale=SCALE,
                    coordinate_transform='100 * mirrorX(UnityWorld - sourceMothershipWorld); route points use complete TransformPoint hierarchy.',
                    rotation='mirror-X quaternion to XYZ Euler; native heading/roll requires visual validation.',
                    mission_order=[r['mission'] for r in records], missions=records,
                    native_mapping={str(t):dict(definition=q.SHIPS[t]['name'],hull=h,status=status,native_source=str(native_path(h).relative_to(ROOT))) for t,(h,status) in HULLS.items()},
                    unique_dependencies=DEPENDENCIES,
                    addSquadron_arguments=dict(argument6=1,argument6_semantics='Not proven by native examples. Explicit per-body calls; no buildBatch/squadronSize inference.',
                                               argument7='1 deferred (native sleeping/hyperspace pattern), 0 initial.',
                                               engine_count_check='VRE_EXPORT logs requested_hulls and SobGroup_Count; engine validation pending.'),
                    source_scripts=['tools/write_quest_progression.py','local/decompiled-demo/Hercules/LoadoutSpawner.cs',
                                    'local/decompiled-demo/Hercules.Designer/Route.cs','local/decompiled-demo/Hercules.Designer.Mission/PatrolManager.cs'],
                    limits=['Inspection scaffold, not complete Visual Scripting port.','No automatic mission victory or objective completion.',
                            'Missing condition adapter blocks its branch.','Pending instant source commands are logged and recorded without claimed implementation.',
                            'Carryover saves, adaptive fleet value, original balance and repeated dynamic waves pending.'])
    save(MANIFEST,manifest)
    write_document(manifest)
    print(json.dumps(dict(missions=len(records),order=manifest['mission_order'],groups=sum(len(r['groups']) for r in records),
                          requested_bodies=sum(len(g['units']) for r in records for g in r['groups']),
                          resource_placements=sum(len(r['resources']) for r in records),
                          missing_unique_instances=sum(len(r['dependencies']) for r in records)),ensure_ascii=False,indent=2))


def write_document(manifest):
    lines = ['# Скриптовая подготовка полной кампании Quest для HWRM','',
             'Экспорт содержит 12 настоящих карт `.level`, стартовые `.lua`, размещения и реестр исходных графов. Обучение T1 идёт первым, затем сохранён порядок MissionDatabase Quest. Это база для ручной проверки и дальнейшего переноса условий; игра и лаунчер не запускались.','',
             '## Состав и порядок','',
             '| № | Глава | Сцена Quest | Группы / корпуса-запросы | Астероиды и объекты ресурсов | Отсутствующие уникальные экземпляры |',
             '|---|---|---|---|---|---|']
    for i,r in enumerate(manifest['missions'],1):
        lines.append(f"| {i} | `{r['directory']}` | `{r['scene']}` | {len(r['groups'])} / {sum(len(g['units']) for g in r['groups'])} | {len(r['resources'])} | {len(r['dependencies'])} |")
    lines += ['', 'Все главы открыты для выбора (`contentOrdered=0`), поскольку условия завершения ещё не перенесены. В коде нет автоматической победы, завершения задачи по таймеру или отладочного пропуска условия. Порядок списка остаётся сюжетным.','',
              '## Размещения','',
              '- Масштаб карты: 100 единиц HWRM на единицу Unity; X отражён, начало — исходная позиция Материнского корабля. Маршруты преобразованы полным TransformPoint с учётом родителей, вращения и масштаба.',
              '- DefaultGroups и AdditionalGroups стоят в настоящих слотах LoadoutSpawner; шаблонные нулевые координаты префабов не приняты за мировую позицию. Это отдельный старт без сохранения переноса флота. AdditionalGroups добавлены после DefaultGroups, как в исходном BuildLoadout.',
              '- Проверяются m_Enabled и активность GameObject по всей иерархии. Статические авто-группы отделены от script_deferred и вариантов патруля.',
              '- Отложенные корпуса имеют последний флаг addSquadron=1 и отдельные spawn volumes. Они не создаются активными и не выключаются массовым Despawn в OnInit. Используется штатная схема Tanis: Vgr_Bomber5/6 → Vgr_Bombers → SobGroup_Spawn.',
              '- Каждый VR SquadronCount развёрнут в явные запросы отдельных корпусов, объединённых SOB-группой; учтены 3 разведчика/корвета и 5 истребителей/бомбардировщиков. Родной buildBatch не переименован в размер VR-отряда. Фактическое число корпусов ещё требует engine-проверки по журналу.',
              '- addToSOBGroup имеет порядок (имя корабля, имя SOB-группы), как в штатных level. Есть сборные VREX_Player/VREX_Enemy/VREX_FriendlyNPC/VREX_Neutral и VREX_Mothership.',
              '- TeamId 1 → игрок0; 1024 → враг1; Player2/TeamId2 → союзный NPC2; None/0 → нейтральный3. Нейтральная сторона союзна остальным, её AI выключен. Это адаптация отношений к игрокам HWRM, а не нейтральная фракция Unity в движке HWRM.',
              '- Нативные Asteroid_4 имеют точный множитель исходных RU/18000. Нулевые астероиды используют Asteroid_1 с resourceValue=0: ресурсы не добавляются искусственно. Радиоактивные/невидимые/отложенные props сохраняются в реестре без произвольной замены.',
              '- DetectionSphere, VisionSphereInitializer и MapCoordinates представлены геометрическими сферами; сами события обнаружения/захвата/обзора пока не реализованы. Все настройки исходника сохранены в placements.json.',
              '- Патруль выбирает один вариант состава и spawn pose; не суммирует альтернативы. Маршрут движется по исходным мировым точкам. Повторные экземпляры, занятость/free-route pool и адаптивное усиление не выданы за восстановленную систему.','',
              '## Шестой аргумент addSquadron','',
              'В 7473 локальных штатных примерах обнаружены аргументы 0 (7207), 1 (264, только обломки) и два неинициализированных значения -842150451 у ресурсников тестовой карты. Этого недостаточно, чтобы доказать его назначение как «количество корпусов». Поэтому код не выводит численность из buildBatch/squadronSize. Каждый корпус перечислен отдельно с аргументом6=1; журнал печатает requested_hulls и engine_count. Пока они не сверены в движке, это явные запросы на размещение, а не утверждение о проверенной численности родных вэйгровских эскадрилий.','',
              '## Стартовые скрипты и недостающие обработчики','',
              'VREX_Common.lua выполняет OnInit, отключает самостоятельный CPU, настраивает отношения, ограничения строительства/research, статические состояния и автоматические патрули. Далее запускает только управляющие ветви OnSimReady главного графа. Sequence обходит ветви последовательно; WaitForSeconds сохраняет настоящую задержку, PlayDialogue использует VRE_PlayLine/VRE_Text/VRE_Duration, AddObjective добавляет исходную задачу. SpawnEntity разрешён в исходный спавнер, а не в выдуманную волну.','',
              'Вступления привязаны по настоящей цепочке PlayableDirector → TimelineAsset → AnimaticCaptionTrack → DialogueAudioAsset → DialogueLine: сохранены исходные начала и длительности клипов. Общий пролог M1 воспроизводится только в T1; в M1 дубля нет. Во время вступления начальные корабли временно неподвижны и неуязвимы, стройка закрыта; затем возвращаются исходные статические состояния и запускаются OnSimReady. Финальный M14 сохранён в outro-реестре M13, но без настоящего условия победы не проигрывается автоматически. Это субтитры с исходной разметкой, не готовый перенос Unity-роликов или FDA-озвучки.','',
              'Неперенесённое условие (If с неизвестным вычислением, WaitForLessonCompleted, DetectShip, таймерные циклы, ожидание захвата и т. п.) останавливает именно свою ветвь. Оно никогда не считается выполненным автоматически. Регистрации Health/Loss и VR-команды без адаптера отмечаются PENDING; их исходные аргументы и связи сохранены, но их действия не объявлены работающими. Например, ModifyHealth не наносит скрыто придуманный урон, EnableAttach не создаёт несуществующие точки стыковки.','',
              'В каждой главе VREX_SourceBindings.json содержит команды, условия, reference/source IDs, defaultValues, выражения value-рёбер, управляющие связи, метки редактора и ближайший исходный контекст. VREX_Nodes в Setup.lua — исполнимая часть реестра. VREX_SourceEvent(id) существует для будущего настоящего обработчика события; он не привязан к клавише обхода.','',
              'Строительный whitelist взят из настоящего BuildCommandController (включая blacklist и исключение debugOnly). Разрешены его сопоставленные роли; остальные кушанские варианты и все исследования ограничены. Чужие корпуса Hgn/Vgr не становятся автоматически элементом кушанского build tree; родные prerequisites и новая строительная конфигурация остаются задачей адаптации. Никакие исследования или захваченные технологии не выдуманы по сюжетной реплике.','',
              '### Неперенесённые подключённые узлы по главам','',
              '| Глава | Типы с числом подключённых узлов |','|---|---|']
    for r in manifest['missions']:
        lines.append('| '+r['mission']+' | '+', '.join(f'`{k}` ×{v}' for k,v in sorted(r['unsupported_connected_nodes'].items()))+' |')
    lines += ['', '## Корпуса и зависимости','',
              'За основу взяты штатные кушанские корабли и подтверждённые таииданские/вэйгровские аналоги. Сопоставление по роли отдельно помечено: MissileCorvette Радаа остаётся ракетным по исходной роли, несмотря на таииданский силуэт; MissileFrigate не получает захват только из-за похожести на infiltrator. Инженерный корвет использует salvage-корпус без заявления о готовом ремонте; переработчик Радаа не получил Harvest автоматически. Баррикадный фрегат использует близкую роль Hgn DefenseField, баллистический эсминец — Kus MissileDestroyer; внешний вид и точные способности различаются.','',
              '| Исходный тип | Неподключённая зависимость |','|---|---|']
    for t,reason in DEPENDENCIES.items():
        lines.append('| `'+q.SHIPS[t]['name']+'` | '+reason+' |')
    lines += ['', 'Уникальные объекты имеют пустую SOB-группу и геометрическую отметку места. Нет подмены станции «Раскол» случайной штатной станцией и ложного «готового» финала. Конкретные отсутствующие экземпляры, роли native_mapping, полные составы и исходные ссылки находятся в [placements.json](</C:/Users/Dmitry/Documents/ChatGPT/Homeworld Vast Reaches/campaign-export/manifests/placements.json>).','',
              '## Проверка и продолжение','',
              'Генератор: [prepare_campaign_export.py](</C:/Users/Dmitry/Documents/ChatGPT/Homeworld Vast Reaches/tools/prepare_campaign_export.py>). Запуск: `.\\.venv\\Scripts\\python.exe -X utf8 tools/prepare_campaign_export.py`. Он использует существующие local/quest-campaign, local/quest-audit и helpers write_quest_progression; нового извлечения или установки нет.','',
              'В этой подготовке проверяются порядок/число глав, существование каждого нативного .ship, точное разворачивание SquadronCount, разделение initial/deferred, ссылки спавнеров и структура карт. Отдельно выполняется проверка синтаксиса Lua и OnInit в заглушках API; она не заменяет тест движка.','',
              'Для следующего ручного этапа: подтвердить численность корпусов и ориентации; подключить уникальные корпуса; перенести настоящие условия задачи/захвата/щитовых генераторов/таймеров поражения; восстановить переходы и carryover. Пока этого нет, экспорт годится для осмотра расстановки и проверки привязок, а не для прохождения всей кампании.','']
    (ROOT/'docs/CAMPAIGN_EXPORT_SCRIPTS.md').write_text('\n'.join(lines),encoding='utf8')
    if (ROOT/'local/cinematic-update/integration.json').exists():
        from apply_campaign_movies import add_wrappers, bind_full
        movies=json.loads((ROOT/'campaign-export/cinematics/index.json').read_text(encoding='utf8'))['scenes']
        add_wrappers(ROOT/'campaign-export/data',movies)
        bind_full(ROOT/'campaign-export/data',movies)


if __name__=='__main__':
    main()
