-- M0 presentation. HW1 post-NIS ambience (The Beginning), new camera arcs.
-- Start on the first simulation tick, after the separate prologue movie.
function VRC_TrainingBegin()
    VRC_TrainingIntroductionStarted = 1
    VRC_TrainingOrbitIndex = 1
    VRC_TrainingNextCamera = VRC_Time+6
    Sound_MusicPlayType("data:sound/music/battle/A01_mission1and16",MUS_Ambient)
    Camera_SetLetterboxStateNoUI(1,1)
    Camera_AllowControl(0)
    Universe_AllowPlayerOrders(0)
    Sensors_EnableToggle(0)
    Camera_Interpolate("here","VRC_IntroOrbit_1",6)
end

function VRC_TrainingOrbitUpdate()
    if VRC_Time < VRC_TrainingNextCamera then return end
    VRC_TrainingOrbitIndex = VRC_TrainingOrbitIndex+1
    if VRC_TrainingOrbitIndex > 8 then VRC_TrainingOrbitIndex = 1 end
    Camera_Interpolate("here","VRC_IntroOrbit_"..VRC_TrainingOrbitIndex,6)
    VRC_TrainingNextCamera = VRC_Time+6
end

function VRC_TrainingEnd()
    Camera_Interpolate("here","VRC_HomeCamera",2)
    VRC_RestoreGameplay()
end
