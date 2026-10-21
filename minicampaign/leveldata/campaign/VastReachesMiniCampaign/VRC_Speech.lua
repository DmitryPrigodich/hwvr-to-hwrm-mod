-- Native Subtitle_Add uses ui/subtitle.lua themes and numbered PCM WAVs.
VRC_Speech = {["M01_020_010_FI"]={actor=29,duration=3.258005},["M01_020_035_FI"]={actor=29,duration=7.183333},["M01_025_010_FI"]={actor=29,duration=11.45},["M01_025_020_FI"]={actor=29,duration=5.562018},["M01_030_010_GR"]={actor=30,duration=11.45},["M01_030_040_GR"]={actor=30,duration=9.38068},["M01_035_010_FI"]={actor=29,duration=3.343333},["M01_040_010_FI"]={actor=29,duration=3.258005},["M01_050_010_FI"]={actor=29,duration=3.13},["M01_050_020_KS"]={actor=28,duration=7.418005},["M01_060_010_AR"]={actor=31,duration=8.996667},["M01_060_030_AR"]={actor=31,duration=10.362018},["M01_060_040_KS"]={actor=28,duration=2.468685},["M01_060_050_AR"]={actor=31,duration=8.036667},["M01_060_055_AR"]={actor=31,duration=8.783333},["M01_060_090_TS"]={actor=27,duration=8.71932},["M01_070_010_FI"]={actor=29,duration=7.46068},["M01_070_020_KS"]={actor=28,duration=6.436667},["M01_070_030_TS"]={actor=27,duration=13.476667},["M04_020_010_KS"]={actor=28,duration=4.665986},["M04_020_040_KS"]={actor=28,duration=9.21},["M04_030_010_FI"]={actor=29,duration=5.54068},["M04_040_010_FI"]={actor=29,duration=3.258005},["M04_040_030_TS"]={actor=27,duration=6.65},["M04_050_010_FI"]={actor=29,duration=4.922018},["M04_050_020_KS"]={actor=28,duration=4.751338},["M04_060_010_FI"]={actor=29,duration=6.18068},["M04_060_030_KS"]={actor=28,duration=9.423333},["M04_070_010_FI"]={actor=29,duration=4.73},["M04_080_010_FI"]={actor=29,duration=7.418005},["M04_100_020_FI"]={actor=29,duration=5.37},["T01_010_010_TS"]={actor=27,duration=6.202018},["T01_010_020_KS"]={actor=28,duration=10.191338},["T01_010_030_TS"]={actor=27,duration=11.172653},["T01_010_040_KS"]={actor=28,duration=7.076667},["T01_020_010_FI"]={actor=29,duration=7.738005},["T01_020_020_FI"]={actor=29,duration=5.455351},["T01_020_030_FI"]={actor=29,duration=7.844671},["T01_020_040_FI"]={actor=29,duration=5.156667},["T01_020_050_TS"]={actor=27,duration=7.29},["T01_020_060_KS"]={actor=28,duration=5.305986},["T01_030_010_FI"]={actor=29,duration=9.21},["T01_030_013_FI"]={actor=29,duration=3.514014},["T01_030_017_FI"]={actor=29,duration=3.684671},["T01_030_040_TS"]={actor=27,duration=9.615351},["T01_030_050_KS"]={actor=28,duration=11.385986},["T01_040_010_FI"]={actor=29,duration=10.212653},["T01_040_020_FI"]={actor=29,duration=3.087347},["T01_040_035_FI"]={actor=29,duration=3.492653},["T01_040_050_FI"]={actor=29,duration=6.543333},["T01_040_060_KS"]={actor=28,duration=2.767347},["T01_040_070_TS"]={actor=27,duration=6.138005},["T01_040_080_KS"]={actor=28,duration=7.631338},["T01_050_040_KS"]={actor=28,duration=5.092653},["T01_050_050_TS"]={actor=27,duration=5.647347},["T01_050_060_KS"]={actor=28,duration=6.607347},["T01_060_010_FI"]={actor=29,duration=5.498005},["T01_060_020_FI"]={actor=29,duration=5.796667},["T01_060_030_FI"]={actor=29,duration=3.364671},["T01_070_010_KS"]={actor=28,duration=12.23932},["T01_070_020_KS"]={actor=28,duration=1.785986},["T01_070_030_TS"]={actor=27,duration=9.70068},["T01_070_040_KS"]={actor=28,duration=7.61},["T01_070_050_TS"]={actor=27,duration=8.847347},["T01_070_060_TS"]={actor=27,duration=7.311338}}
function VRC_LineReady()
    if VRC_ActiveActor ~= nil then return Subtitle_IsDone(VRC_ActiveActor) end
    if VRC_Time >= VRC_NextLine then return 1 end
    return 0
end
function VRC_QueueDone()
    if VRC_QueueIndex > getn(VRC_Queue) and VRC_LineReady() ~= 0 then return 1 end
    return 0
end
function VRC_PlayLine(key,duration)
    local speech=VRC_Speech[key]
    VRC_ActiveActor=nil
    if speech ~= nil then
        VRC_ActiveActor=speech.actor
        Subtitle_Add(speech.actor,VRC_Text[key],speech.duration)
        return speech.duration
    end
    Subtitle_Message(VRC_Text[key],duration)
    return duration
end
function VRC_KeepDialogueAndFinish(key)
    local pending={}
    for i=VRC_QueueIndex,getn(VRC_Queue) do
        local queued=VRC_Queue[i]
        if VRC_Speech[queued] ~= nil then pending[getn(pending)+1]=queued end
    end
    VRC_Queue=pending
    VRC_QueueIndex=1
    VRC_Line(key)
end
