function NKR_SensorUpdate(group, playerIndex, shipID)
    local enabled = Player_HasResearch(playerIndex, "NKR_HyperspaceSensors")
    SobGroup_SetHardPointHealth(group, "NKR Hyperspace Sensor", enabled)
end
