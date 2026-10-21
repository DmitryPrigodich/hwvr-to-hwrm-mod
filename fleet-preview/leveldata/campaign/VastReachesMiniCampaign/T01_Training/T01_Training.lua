dofilepath("data:leveldata/campaign/VastReachesMiniCampaign/T01_Training/VRC_Setup.lua")
dofilepath("data:leveldata/campaign/VastReachesMiniCampaign/VRC_Common.lua")

function OnInit()
    VRC_Init({"Kus_Interceptor"})
    VRC_IntroLock = 1
    VRC_Lines({"prototype","M01_010_010_A_HA","M01_010_020_A_HA","M01_010_030_A_HA","M01_010_040_A_HA","M01_010_050_A_HA","M01_010_060_A_HA","M01_010_070_A_HA","M01_010_080_A_HA","T01_010_010_TS","T01_010_020_KS","T01_010_030_TS","T01_010_040_KS"})
    VRC_NewObjective("t_move","VRC_MovePoint_Camera")
end

function VRC_Update()
    -- Let the prologue and first connection finish before exercise progression.
    if VRC_IntroLock == 1 then
        if VRC_QueueIndex <= getn(VRC_Queue) or VRC_Time < VRC_NextLine then return end
        VRC_IntroLock = 0
    end
    if VRC_State == 1 then
        Player_FillShipsByType("VRC_Temp",0,"Kus_Interceptor")
        if VRC_AtVolume("VRC_Temp","VRC_MovePoint") then
            VRC_Show("VRC_TrainingA")
            VRC_NewObjective("t_attack","VRC_TargetPoint_Camera")
        end
    elseif VRC_State == 2 then
        if not VRC_Alive("VRC_TrainingA") then
            VRC_Baseline = Player_GetNumberOfSquadronsOfTypeAwakeOrSleeping(0,"Kus_Interceptor")
            VRC_NewObjective("t_build","VRC_HomeCamera")
        end
    elseif VRC_State == 3 then
        if Player_GetNumberOfSquadronsOfTypeAwakeOrSleeping(0,"Kus_Interceptor")>VRC_Baseline then
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
