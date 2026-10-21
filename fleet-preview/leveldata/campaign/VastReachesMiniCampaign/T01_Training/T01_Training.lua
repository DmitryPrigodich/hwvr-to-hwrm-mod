dofilepath("data:leveldata/campaign/VastReachesMiniCampaign/T01_Training/VRC_Setup.lua")
dofilepath("data:leveldata/campaign/VastReachesMiniCampaign/VRC_Common.lua")
dofilepath("data:leveldata/campaign/VastReachesMiniCampaign/T01_Training/VRC_TrainingPresentation.lua")

function OnInit()
    VRC_Init({"Kus_Scout"})
    VRC_IntroLock = 1
    VRC_TrainingPhase = 1
    VRC_SensorsSeen = 0
    VRC_TrainingIntroductionStarted = 0
    VRC_Lines({"T01_010_010_TS","T01_010_020_KS","T01_010_030_TS","T01_010_040_KS"})
end

function VRC_Update()
    -- Let the prologue and first connection finish before exercise progression.
    if VRC_IntroLock == 1 then
        if VRC_TrainingIntroductionStarted == 0 then VRC_TrainingBegin() end
        if VRC_TrainingPhase == 1 then
            VRC_TrainingOrbitUpdate()
            if VRC_QueueDone() == 0 then return end
            VRC_TrainingEnd()
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
            VRC_NewObjective("t_move","VRC_MovePoint_Camera")
        end
        return
    end
    if VRC_State == 1 then
        Player_FillShipsByType("VRC_Temp",0,"Kus_Scout")
        if VRC_AtVolume("VRC_Temp","VRC_MovePoint") then
            VRC_Show("VRC_TrainingA")
            VRC_NewObjective("t_attack","VRC_TargetPoint_Camera")
        end
    elseif VRC_State == 2 then
        if not VRC_Alive("VRC_TrainingA") then
            VRC_Baseline = Player_GetNumberOfSquadronsOfTypeAwakeOrSleeping(0,"Kus_Scout")
            VRC_NewObjective("t_build","VRC_HomeCamera")
        end
    elseif VRC_State == 3 then
        if Player_GetNumberOfSquadronsOfTypeAwakeOrSleeping(0,"Kus_Scout")>VRC_Baseline then
            VRC_Show("VRC_TrainingB")
            VRC_Show("VRC_TrainingC")
            VRC_Show("VRC_Platform")
            VRC_Attack("VRC_TrainingB","VRC_Mothership")
            VRC_Attack("VRC_TrainingC","VRC_Mothership")
            VRC_NewObjective("t_final","VRC_MovePoint_Camera")
        end
    elseif VRC_State == 4 then
        if not VRC_Alive("VRC_TrainingB") and not VRC_Alive("VRC_TrainingC") and not VRC_Alive("VRC_Platform") then
            VRC_Win("t_done")
        end
    end
end
