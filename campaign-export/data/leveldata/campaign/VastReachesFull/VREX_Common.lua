-- Conservative Lua 4-compatible inspection runtime; no automatic victory.
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
