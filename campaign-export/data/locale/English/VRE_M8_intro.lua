-- Experimental flat adaptation of the original VR scene.
MovieScreen = {
    displayName = "$9950146",
    helpTip = "$9950146",
    Layout = {size_WH = {w=1,h=1,wr="scr",hr="scr"}},
    stylesheet = "HW2StyleSheet",
    RootElementSettings = {backgroundColor={0,0,0,255}},
    speechFilename="locale:VRE_M8_intro_speech.lua",
    [1] = {
        type="Movie", name="MyMovie",
        filenameV="data:animatics/VastReaches/English/VRE_M8_intro.webm",
        Layout = {
            pos_XY={x=0.5,y=0.5,xr="par",yr="par"}, pivot_XY={0.5,0.5},
            lockAspect=1280/720,
            size_WH={w=100000,h=1,wr="px",hr="par"},
            max_WH={w=1,h=1,wr="par",hr="par"},
        },
        fixedAspectRatio=1, greyScale=0, abortFadeOutLength=0.25,
        volumemultiplier=0.88,
    },
}
