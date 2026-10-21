-- M0 presentation. HW1 post-NIS ambience (The Beginning), new camera arcs.
-- Start on the first simulation tick, after the separate prologue movie.
function VRC_TrainingBegin()
    VRC_TrainingIntroductionStarted = 1
    VRC_TrainingOrbitIndex = 1
    VRC_TrainingNextCamera = VRC_Time+4
    Sound_MusicPlayType("data:sound/music/battle/A01_mission1and16",MUS_Ambient)
    Camera_SetLetterboxStateNoUI(1,1)
    Camera_AllowControl(0)
    Universe_AllowPlayerOrders(0)
    Sensors_EnableToggle(0)
    Camera_Interpolate("here","VRC_IntroOrbit_1",4)
end

function VRC_TrainingOrbitUpdate()
    if VRC_Time < VRC_TrainingNextCamera then return end
    VRC_TrainingOrbitIndex = VRC_TrainingOrbitIndex+1
    if VRC_TrainingOrbitIndex > 32 then VRC_TrainingOrbitIndex = 1 end
    Camera_Interpolate("here","VRC_IntroOrbit_"..VRC_TrainingOrbitIndex,4)
    VRC_TrainingNextCamera = VRC_Time+4
end

function VRC_TrainingEnd()
    -- Finish the current short arc without pulling the view back to HomeCamera.
    -- From Fleet Intelligence onward, no further camera orders are issued.
    VRC_RestoreGameplay()
end
