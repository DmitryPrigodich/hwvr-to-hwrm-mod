-- HWRM Lua 4-compatible subset. Script-only adaptation, not a complete VR port.
dofilepath("data:scripts/SCAR/SCAR_Util.lua")
dofilepath("data:leveldata/campaign/VastReachesMiniCampaign/VRC_Data.lua")

function VRC_Init(allowed)
    VRC_Time = 0
    VRC_State = 0
    VRC_Ended = 0
    VRC_Queue = {}
    VRC_QueueIndex = 1
    VRC_NextLine = 0
    VRC_Objective = -1
    VRC_Optional = -1
    VRC_Focus = "VRC_HomeCamera"
    VRC_StageTime = 0
    VRC_Ping = -1
    CPU_Enable(1,0)
    CPU_Enable(2,0)
    SetAlliance(1,2)
    SetAlliance(2,1)
    SetAlliance(0,2)
    SetAlliance(2,0)
    SobGroup_Create("VRC_Temp")
    SobGroup_Create("VRC_Near")
    SobGroup_Create("VRC_Engineers")
    SobGroup_Create("VRC_Scouts")
    SobGroup_Create("VRC_InVolume")
    for i=1,getn(VRC_Hidden) do SobGroup_Despawn(VRC_Hidden[i]) end
    for i=1,getn(VRC_AllBuilds) do Player_RestrictBuildOption(0,VRC_AllBuilds[i]) end
    for i=1,getn(VRC_AllResearch) do Player_RestrictResearchOption(0,VRC_AllResearch[i]) end
    for i=1,getn(allowed) do Player_UnrestrictBuildOption(0,allowed[i]) end
    Player_GrantResearchOption(0,"FighterChassis")
    if VRC_Mission == "M04_LostDestroyer" then
        Player_GrantResearchOption(0,"CorvetteChassis")
        Player_GrantResearchOption(0,"HeavyCorvetteUpgrade")
    end
    -- The stock Kushan hull's docking, guns and build bays remain native.
    SobGroup_AbilityActivate("VRC_Mothership",AB_Move,0)
    UI_BindKeyEvent(ONEKEY,"VRC_ViewHome")
    UI_BindKeyEvent(TWOKEY,"VRC_ViewObjective")
    Camera_Interpolate("here","VRC_HomeCamera",0)
    Rule_AddInterval("VRC_Tick",1)
    print("VRC_MINI: init "..VRC_Mission)
end

function VRC_ViewHome()
    Camera_Interpolate("here","VRC_HomeCamera",0)
end

function VRC_ViewObjective()
    Camera_Interpolate("here",VRC_Focus,0)
end

function VRC_Line(key)
    if VRC_Text[key] ~= nil then
        VRC_Queue[getn(VRC_Queue)+1] = key
    else
        print("VRC_MINI: missing text "..key)
    end
end

function VRC_Lines(keys)
    for i=1,getn(keys) do VRC_Line(keys[i]) end
end

function VRC_NewObjective(key,focus)
    if VRC_Objective ~= -1 then Objective_SetState(VRC_Objective,OS_Complete) end
    VRC_Objective = Objective_Add(VRC_Text[key],OT_Primary)
    VRC_State = VRC_State+1
    VRC_StageTime = VRC_Time
    if focus ~= nil then VRC_Focus = focus end
    if VRC_Ping ~= -1 then Ping_Remove(VRC_Ping) end
    if VRC_FocusPoints[VRC_Focus] ~= nil then
        VRC_Ping=Ping_AddPoint(VRC_Text[key],"anomaly",VRC_FocusPoints[VRC_Focus])
    else
        VRC_Ping=Ping_AddSobGroup(VRC_Text[key],"anomaly","VRC_Mothership")
    end
    print("VRC_MINI: stage="..VRC_State.." objective="..key)
end

function VRC_Alive(name)
    return SobGroup_Count(name)>0
end

function VRC_Show(name)
    SobGroup_Spawn(name,name.."_Spawn")
    FOW_RevealGroup(name,1)
end

function VRC_Attack(name,target)
    SobGroup_SetROE(name,OffensiveROE)
    SobGroup_SetStance(name,AggressiveStance)
    SobGroup_Attack(1,name,target)
end

function VRC_AnyPlayerIn(volume)
    Player_FillSobGroupInVolume("VRC_InVolume",0,volume)
    return SobGroup_Count("VRC_InVolume")>0
end

function VRC_AtVolume(group,volume)
    SobGroup_FillSobGroupInVolume("VRC_InVolume",group,volume)
    return SobGroup_Count("VRC_InVolume")>0
end

function VRC_Win(key)
    if VRC_State == 99 then return end
    if VRC_Objective ~= -1 then Objective_SetState(VRC_Objective,OS_Complete) end
    VRC_State = 99
    VRC_EndTime = VRC_Time+14
    VRC_Queue = {}
    VRC_QueueIndex = 1
    VRC_NextLine = VRC_Time
    VRC_Line(key)
    print("VRC_MINI: victory pending "..key)
end

function VRC_Fail(key)
    VRC_Ended = 1
    if VRC_Objective ~= -1 then Objective_SetState(VRC_Objective,OS_Failed) end
    Subtitle_Message(VRC_Text[key],10)
    Rule_Remove("VRC_Tick")
    setMissionComplete(0)
end

function VRC_Tick()
    if VRC_Ended == 1 then return end
    VRC_Time = VRC_Time+1
    if not VRC_Alive("VRC_Mothership") then VRC_Fail("loss") return end
    if VRC_State == 99 then
        if VRC_Time >= VRC_EndTime then
            VRC_Ended = 1
            Rule_Remove("VRC_Tick")
            setMissionComplete(1)
        end
    else
        VRC_Update()
    end
    if VRC_Ended == 0 and VRC_Time >= VRC_NextLine and VRC_QueueIndex <= getn(VRC_Queue) then
        local key=VRC_Queue[VRC_QueueIndex]
        local duration=VRC_Duration[key]
        Subtitle_Message(VRC_Text[key],duration)
        VRC_QueueIndex = VRC_QueueIndex+1
        VRC_NextLine = VRC_Time+duration
    end
end
