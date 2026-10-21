-- Repeatable, non-lethal waypoint lesson. Native COMMAND_WaypointMove is
-- distinguished from COMMAND_Move by SCAR/kasutil.lua's command mapping.
function VRC_TrainingRouteReset(message)
    SobGroup_Stop(0,"VRC_Scouts")
    SobGroup_Despawn("VRC_Scouts")
    SobGroup_Spawn("VRC_Scouts","VRC_RouteStart")
    SobGroup_SetInvulnerability("VRC_Scouts",1)
    SobGroup_SetHealth("VRC_Scouts",1)
    SobGroup_AbilityActivate("VRC_Scouts",AB_Attack,0)
    SobGroup_SetROE("VRC_Scouts",PassiveROE)
    VRC_RouteProgress = 0
    VRC_RouteComplete = 0
    if message ~= nil then
        VRC_RouteRetries = VRC_RouteRetries+1
        Subtitle_Message(VRC_Text[message],9)
    end
end

function VRC_TrainingRouteBegin()
    VRC_Show("VRC_Platform")
    SobGroup_AbilityActivate("VRC_Platform",AB_Attack,0)
    SobGroup_AbilityActivate("VRC_Platform",AB_Move,0)
    SobGroup_SetInvulnerability("VRC_Platform",1)
    VRC_RouteRetries = 0
    VRC_TrainingRouteReset(nil)
    VRC_RoutePings = {
        Ping_AddPoint(VRC_Text["t_route_a"],"anomaly","VRC_RouteA"),
        Ping_AddPoint(VRC_Text["t_route_b"],"anomaly","VRC_RouteB"),
        Ping_AddPoint(VRC_Text["t_route_danger"],"anomaly","VRC_GunZone")
    }
    VRC_NewObjective("t_route","VRC_RoutePoint_Camera")
end

function VRC_TrainingRouteUpdate()
    if VRC_RouteComplete == 1 then return 1 end
    -- The 3500 m sphere is outside the stock gun's maximum 2950 m range.
    -- Invulnerability prevents casualties between the one-second checks.
    if VRC_AtVolume("VRC_Scouts","VRC_GunZone") then
        VRC_TrainingRouteReset("t_route_retry")
        return 0
    end
    if SobGroup_GetCurrentOrder("VRC_Scouts") == COMMAND_WaypointMove then
        if VRC_RouteProgress == 0 and VRC_AtVolume("VRC_Scouts","VRC_RouteA") then
            VRC_RouteProgress = 1
        elseif VRC_RouteProgress == 1 and VRC_AtVolume("VRC_Scouts","VRC_RouteB") then
            VRC_RouteProgress = 2
        end
    end
    if VRC_AtVolume("VRC_Scouts","VRC_RoutePoint") then
        if VRC_RouteProgress == 2 then
            VRC_RouteComplete = 1
            SobGroup_Stop(0,"VRC_Scouts")
            return 1
        end
        VRC_TrainingRouteReset("t_route_required")
    end
    return 0
end

function VRC_TrainingRouteEnd()
    for i=1,getn(VRC_RoutePings) do Ping_Remove(VRC_RoutePings[i]) end
    SobGroup_AbilityActivate("VRC_Platform",AB_Attack,0)
    SobGroup_SetInvulnerability("VRC_Scouts",0)
    SobGroup_AbilityActivate("VRC_Scouts",AB_Attack,1)
    SobGroup_SetROE("VRC_Scouts",OffensiveROE)
end
