dofilepath("data:leveldata/campaign/VastReachesMiniCampaign/T01_Training/VRC_Setup.lua")
dofilepath("data:leveldata/campaign/VastReachesMiniCampaign/VRC_Common.lua")
dofilepath("data:leveldata/campaign/VastReachesMiniCampaign/T01_Training/VRC_TrainingPresentation.lua")
dofilepath("data:leveldata/campaign/VastReachesMiniCampaign/T01_Training/VRC_TrainingRoute.lua")

function OnInit()
    VRC_Init({})
    VRC_IntroLock = 1
    VRC_TrainingPhase = 1
    VRC_SensorsSeen = 0
    VRC_TrainingIntroductionStarted = 0
    -- Stock Speed Burst is a CustomCommand. It is not part of this systems test.
    Player_RestrictBuildOption(0,"Kus_Scout")
    SobGroup_AbilityActivate("VRC_Mothership",AB_Builder,0)
    VRC_TrainingNoBurst()
    VRC_Lines({"T01_010_010_TS","T01_010_020_KS","T01_010_030_TS","T01_010_040_KS"})
end

function VRC_TrainingNoBurst()
    Player_FillShipsByType("VRC_Scouts",0,"Kus_Scout")
    SobGroup_AbilityActivate("VRC_Scouts",AB_Custom,0)
    SobGroup_AbilityActivate("VRC_Scouts",AB_Retire,0)
    SobGroup_AbilityActivate("VRC_Scouts",AB_Scuttle,0)
end

function VRC_Update()
    VRC_TrainingNoBurst()
    if not VRC_Alive("VRC_Scouts") then VRC_Fail("t_fighters_lost") return end
    -- Let the prologue and first connection finish before exercise progression.
    if VRC_IntroLock == 1 then
        if VRC_TrainingIntroductionStarted == 0 then VRC_TrainingBegin() end
        if VRC_TrainingPhase == 1 then
            if VRC_QueueDone() == 0 then
                VRC_TrainingOrbitUpdate()
                return
            end
            -- Let the last short arc finish before Fleet Intelligence starts.
            if VRC_Time < VRC_TrainingNextCamera then return end
            VRC_TrainingEnd()
            VRC_SetObjective("t_sensors","VRC_HomeCamera")
            VRC_Lines({"T01_020_010_FI","T01_020_020_FI"})
            VRC_TrainingPhase = 2
        elseif VRC_TrainingPhase == 2 then
            if Sensors_ManagerIsActive() ~= 0 then VRC_SensorsSeen = 1 end
            if VRC_QueueDone() == 0 or VRC_SensorsSeen == 0 then return end
            VRC_Lines({"T01_020_030_FI","T01_020_040_FI","T01_020_050_TS","T01_020_060_KS"})
            VRC_TrainingPhase = 3
        elseif VRC_TrainingPhase == 3 then
            if VRC_QueueDone() == 0 then return end
            VRC_IntroLock = 0
            VRC_TrainingPhase = 4
            Camera_ResetRotated()
            VRC_Lines({"T01_030_010_FI"})
            VRC_NewObjective("t_rotate","VRC_HomeCamera")
        end
        return
    end
    if VRC_State == 1 then
        if VRC_QueueDone() ~= 0 and Camera_PlayerHasRotated(0.0) ~= 0 then
            VRC_TrainingZoom = Camera_GetLastZoomAmount()
            VRC_Line("T01_030_013_FI")
            VRC_NewObjective("t_zoom","VRC_HomeCamera")
        end
    elseif VRC_State == 2 then
        if VRC_QueueDone() ~= 0 and Camera_GetLastZoomAmount() ~= VRC_TrainingZoom then
            Camera_UsePanning(1)
            Camera_ResetPanned()
            VRC_Line("T01_030_017_FI")
            VRC_NewObjective("t_pan","VRC_HomeCamera")
        end
    elseif VRC_State == 3 then
        -- VR teleport line T01_030_020_FI is kept in the source reader, not played on PC.
        if VRC_QueueDone() ~= 0 and Camera_PlayerHasPanned(0.01) ~= 0 then
            VRC_Lines({"T01_030_040_TS","T01_030_050_KS","T01_040_010_FI"})
            VRC_NewObjective("t_select","VRC_HomeCamera")
        end
    elseif VRC_State == 4 then
        if VRC_QueueDone() ~= 0 and SobGroup_Selected("VRC_Scouts") ~= 0 then
            VRC_Line("T01_040_020_FI")
            VRC_NewObjective("t_move","VRC_MovePoint_Camera")
        end
    elseif VRC_State == 5 then
        if VRC_QueueDone() ~= 0 and VRC_AtVolume("VRC_Scouts","VRC_MovePoint") then
            VRC_Show("VRC_TrainingA")
            SobGroup_SetROE("VRC_TrainingA",PassiveROE)
            SobGroup_AbilityActivate("VRC_TrainingA",AB_Attack,0)
            SobGroup_AbilityActivate("VRC_TrainingA",AB_Move,0)
            VRC_Lines({"T01_040_035_FI","T01_040_050_FI"})
            VRC_NewObjective("t_attack","VRC_TargetPoint_Camera")
        end
    elseif VRC_State == 6 then
        if VRC_QueueDone() ~= 0 and not VRC_Alive("VRC_TrainingA") then
            -- Construction, retirement and multiple-group drills are omitted.
            -- Keep the story conversation about bonding with ships and losses.
            VRC_Lines({"T01_040_060_KS","T01_040_070_TS","T01_040_080_KS","T01_050_040_KS","T01_050_050_TS","T01_050_060_KS","T01_060_010_FI","T01_060_020_FI"})
            VRC_TrainingRouteBegin()
        end
    elseif VRC_State == 7 then
        if VRC_QueueDone() ~= 0 then SobGroup_AbilityActivate("VRC_Platform",AB_Attack,1) end
        local arrived = VRC_TrainingRouteUpdate()
        if arrived ~= 0 and VRC_QueueDone() ~= 0 then
            VRC_TrainingRouteEnd()
            VRC_Show("VRC_TrainingB")
            VRC_Show("VRC_TrainingC")
            Sound_MusicPlayType("data:sound/music/battle/B01_TuranicRaidersLong",MUS_Ambient)
            VRC_Attack("VRC_TrainingB","VRC_Scouts")
            VRC_Attack("VRC_TrainingC","VRC_Scouts")
            VRC_NewObjective("t_final","VRC_BattlePoint_Camera")
        end
    elseif VRC_State == 8 then
        if not VRC_Alive("VRC_TrainingB") and not VRC_Alive("VRC_TrainingC") then
            Sound_MusicPlayType("data:sound/music/battle/A01_mission1and16",MUS_Ambient)
            VRC_Lines({"T01_060_030_FI","T01_070_010_KS","T01_070_020_KS","T01_070_030_TS","T01_070_040_KS","T01_070_050_TS","T01_070_060_TS"})
            VRC_Win("t_done")
        end
    end
end
