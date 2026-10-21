dofilepath("data:leveldata/campaign/VastReachesMiniCampaign/T01_Training/VRC_Setup.lua")
dofilepath("data:leveldata/campaign/VastReachesMiniCampaign/VRC_Common.lua")
dofilepath("data:leveldata/campaign/VastReachesMiniCampaign/T01_Training/VRC_TrainingPresentation.lua")

function OnInit()
    VRC_Init({"Kus_Scout"})
    VRC_IntroLock = 1
    VRC_TrainingPhase = 1
    VRC_SensorsSeen = 0
    VRC_TrainingIntroductionStarted = 0
    -- Stock Speed Burst is a CustomCommand. It is not part of this systems test.
    Player_RestrictBuildOption(0,"Kus_Scout")
    VRC_TrainingNoBurst()
    VRC_Lines({"T01_010_010_TS","T01_010_020_KS","T01_010_030_TS","T01_010_040_KS"})
end

function VRC_TrainingNoBurst()
    Player_FillShipsByType("VRC_Scouts",0,"Kus_Scout")
    SobGroup_AbilityActivate("VRC_Scouts",AB_Custom,0)
end

function VRC_Update()
    VRC_TrainingNoBurst()
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
            VRC_Lines({"T01_040_060_KS","T01_040_070_TS","T01_040_080_KS","T01_050_010_FI","T01_050_020_FI"})
            Player_UnrestrictBuildOption(0,"Kus_Scout")
            VRC_NewObjective("t_build","VRC_HomeCamera")
        end
    elseif VRC_State == 7 then
        -- Pause/retire are optional: paused simulation cannot run a wait rule.
        -- Count squadron entries here, not visible physical hulls within a batch.
        if VRC_QueueDone() ~= 0 and SobGroup_Count("VRC_Scouts") >= 2 then
            VRC_Lines({"T01_050_040_KS","T01_050_050_TS","T01_050_060_KS","T01_040_030_FI","T01_060_010_FI","T01_060_020_FI"})
            VRC_Show("VRC_Platform")
            SobGroup_AbilityActivate("VRC_Platform",AB_Attack,0)
            VRC_NewObjective("t_route","VRC_RoutePoint_Camera")
        end
    elseif VRC_State == 8 then
        if VRC_QueueDone() == 0 then return end
        SobGroup_AbilityActivate("VRC_Platform",AB_Attack,1)
        SobGroup_FillSobGroupInVolume("VRC_InVolume","VRC_Scouts","VRC_RoutePoint")
        if SobGroup_Count("VRC_InVolume") >= 2 then
            VRC_Show("VRC_TrainingB")
            VRC_Show("VRC_TrainingC")
            Sound_MusicPlayType("data:sound/music/battle/B01_TuranicRaidersLong",MUS_Ambient)
            VRC_Attack("VRC_TrainingB","VRC_Scouts")
            VRC_Attack("VRC_TrainingC","VRC_Scouts")
            VRC_NewObjective("t_final","VRC_BattlePoint_Camera")
        end
    elseif VRC_State == 9 then
        if not VRC_Alive("VRC_TrainingB") and not VRC_Alive("VRC_TrainingC") then
            Sound_MusicPlayType("data:sound/music/battle/A01_mission1and16",MUS_Ambient)
            VRC_Lines({"T01_060_030_FI","T01_070_010_KS","T01_070_020_KS","T01_070_030_TS","T01_070_040_KS","T01_070_050_TS","T01_070_060_TS"})
            VRC_Win("t_done")
        end
    end
end
