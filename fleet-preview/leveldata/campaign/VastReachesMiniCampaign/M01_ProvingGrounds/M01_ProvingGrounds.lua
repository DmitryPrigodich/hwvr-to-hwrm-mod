dofilepath("data:leveldata/campaign/VastReachesMiniCampaign/M01_ProvingGrounds/VRC_Setup.lua")
dofilepath("data:leveldata/campaign/VastReachesMiniCampaign/VRC_Common.lua")

function OnInit()
    VRC_Init({"Kus_Interceptor","Kus_AttackBomber","Kus_ResourceCollector"})
    -- The shared story prologue now belongs to T1, before the first campaign mission.
    VRC_Lines({"prototype","M01_020_010_FI","M01_020_035_FI"})
    VRC_NewObjective("M01_Objective_00","VRC_HomeCamera")
end

function VRC_StartPatrol(name)
    VRC_Show(name)
    -- Native stock hull balance is provisional; attack path is an adaptation of VR patrols.
    SobGroup_Move(1,name,"VRC_ScoutPoint")
end

function VRC_Update()
    if VRC_State == 1 then
        if Player_GetRU(0)>=200 then
            Player_UnrestrictBuildOption(0,"Kus_Scout")
            VRC_Lines({"M01_025_010_FI","M01_025_020_FI"})
            VRC_NewObjective("M01_Objective_00a","VRC_HomeCamera")
        end
    elseif VRC_State == 2 then
        if Player_GetNumberOfSquadronsOfTypeAwakeOrSleeping(0,"Kus_Scout")>0 then
            VRC_Lines({"M01_030_010_GR","M01_030_040_GR","scan"})
            VRC_NewObjective("M01_Objective_00b","VRC_ScoutPoint_Camera")
        end
    elseif VRC_State == 3 then
        Player_FillShipsByType("VRC_Scouts",0,"Kus_Scout")
        if VRC_AtVolume("VRC_Scouts","VRC_ScoutPoint") then
            VRC_StartPatrol("VRC_Patrol1")
            VRC_Line("M01_035_010_FI")
            VRC_NewObjective("M01_Objective_01","VRC_ScoutPoint_Camera")
        end
    elseif VRC_State == 4 then
        if not VRC_Alive("VRC_Patrol1") then
            VRC_StartPatrol("VRC_Patrol2")
            VRC_Line("M01_040_010_FI")
            VRC_NewObjective("M01_Objective_01b","VRC_ScoutPoint_Camera")
        end
    elseif VRC_State == 5 then
        if not VRC_Alive("VRC_Patrol2") then
            VRC_StartPatrol("VRC_Patrol3")
            VRC_Lines({"M01_050_010_FI","M01_050_020_KS"})
            VRC_NewObjective("M01_Objective_01c","VRC_ScoutPoint_Camera")
        end
    elseif VRC_State == 6 then
        if not VRC_Alive("VRC_Patrol3") then
            VRC_Lines({"M01_060_010_AR","M01_060_030_AR","M01_060_040_KS","M01_060_050_AR","M01_060_055_AR","M01_060_090_TS"})
            for i=1,3 do
                local name="VRC_Breach"..i
                VRC_Show(name)
                SobGroup_SetHealth(name,0.45)
                VRC_Attack(name,"VRC_Mothership")
            end
            VRC_NewObjective("M01_Objective_02b","VRC_HomeCamera")
            VRC_Optional=Objective_Add(VRC_Text["M01_Objective_02"],OT_Primary)
        end
    elseif VRC_State == 7 then
        if not VRC_Alive("VRC_Breach1") and not VRC_Alive("VRC_Breach2") and not VRC_Alive("VRC_Breach3") then
            VRC_Lines({"M01_070_010_FI","M01_070_020_KS","M01_070_030_TS","escape"})
            VRC_Show("VRC_FinalFleet")
            for i=1,4 do VRC_Show("VRC_LateFrigate"..i) end
            -- The escape is timed, as in the demo; killing this fleet is not required.
            VRC_NewObjective("escape","VRC_HomeCamera")
        end
    elseif VRC_State == 8 then
        if VRC_Time-VRC_StageTime>=20 then
            Objective_SetState(VRC_Optional,OS_Complete)
            VRC_Win("M01_070_030_TS")
        end
    end
end
