dofilepath("data:leveldata/campaign/VastReachesMiniCampaign/M04_LostDestroyer/VRC_Setup.lua")
dofilepath("data:leveldata/campaign/VastReachesMiniCampaign/VRC_Common.lua")

function OnInit()
    VRC_Init({"Kus_Scout","Kus_Interceptor","Kus_AttackBomber","Kus_HeavyCorvette","Kus_SalvageCorvette","Kus_ResourceCollector"})
    VRC_AttachTime=0
    VRC_PursuitWave=0
    SobGroup_AbilityActivate("VRC_Destroyer",AB_Move,0)
    SobGroup_AbilityActivate("VRC_Destroyer",AB_Attack,0)
    SobGroup_SetHealth("VRC_Destroyer",0.65)
    VRC_Lines({"prototype","M04_010_010_A_FI","M04_010_020_A_TS","M04_010_030_A_FI","M04_010_040_A_TS","M04_010_050_A_KS","M04_010_060_A_TS","M04_010_070_A_KS","M04_010_080_A_TS","M04_020_010_KS","M04_020_040_KS"})
    VRC_NewObjective("M04_Objective_01","VRC_SearchPoint_Camera")
end

function VRC_Update()
    if not VRC_Alive("VRC_Destroyer") then VRC_Fail("M04_100_020_FI") return end
    if VRC_State == 1 then
        if VRC_AnyPlayerIn("VRC_SearchPoint") then
            FOW_RevealGroup("VRC_Destroyer",1)
            VRC_Show("VRC_Retrieval")
            VRC_Attack("VRC_Retrieval","VRC_Mothership")
            VRC_Line("M04_030_010_FI")
            VRC_NewObjective("M04_Objective_02","VRC_DestroyerPoint_Camera")
        end
    elseif VRC_State == 2 then
        if not VRC_Alive("VRC_Retrieval") then
            VRC_Lines({"M04_040_010_FI","M04_040_030_TS","engineers"})
            VRC_NewObjective("M04_Objective_03","VRC_DestroyerPoint_Camera")
        end
    elseif VRC_State == 3 then
        Player_FillShipsByType("VRC_Engineers",0,"Kus_SalvageCorvette")
        SobGroup_FillProximitySobGroup("VRC_Near","VRC_Engineers","VRC_Destroyer",1200)
        if SobGroup_Count("VRC_Near")>=3 then VRC_AttachTime=VRC_AttachTime+1 else VRC_AttachTime=0 end
        if VRC_AttachTime>=10 then
            -- Explicit placeholder: proximity + scripted drive, no physical salvage latch yet.
            SobGroup_SwitchOwner("VRC_Destroyer",0)
            SobGroup_AbilityActivate("VRC_Destroyer",AB_Move,1)
            SobGroup_SetMaxSpeed("VRC_Destroyer",80)
            SobGroup_Move(0,"VRC_Destroyer","VRC_Return")
            VRC_Lines({"M04_050_010_FI","M04_050_020_KS","tow","M04_060_010_FI","M04_060_030_KS"})
            VRC_NewObjective("M04_Objective_04","VRC_DestroyerPoint_Camera")
            VRC_Show("VRC_Gate")
            VRC_Show("VRC_GateGuard")
            VRC_Optional=Objective_Add(VRC_Text["M04_Objective_05"],OT_Secondary)
        end
    elseif VRC_State == 4 then
        if not VRC_Alive("VRC_Gate") then
            Objective_SetState(VRC_Optional,OS_Complete)
            VRC_Win("M04_070_010_FI")
            return
        end
        if VRC_AtVolume("VRC_Destroyer","VRC_Return") then
            -- Gate objective remains optional. Do not mark it completed if the gate survived.
            VRC_Win("M04_080_010_FI")
            return
        end
        -- Three source-derived pursuit groups. Spawned once each, no infinite farm/softlock.
        if VRC_Time-VRC_StageTime >= 15+VRC_PursuitWave*45 and VRC_PursuitWave<3 then
            VRC_PursuitWave=VRC_PursuitWave+1
            local name="VRC_Pursuit"..VRC_PursuitWave
            VRC_Show(name)
            VRC_Attack(name,"VRC_Destroyer")
        end
    end
end
