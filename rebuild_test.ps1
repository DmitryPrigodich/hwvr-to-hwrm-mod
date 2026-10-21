param(
    [switch]$Models,
    [switch]$Recover,
    [switch]$Catalogue,
    [string]$DemoRoot = 'C:\Program Files (x86)\Steam\steamapps\common\Homeworld Vast Reaches Demo',
    [string]$ToolkitRoot = 'C:\Program Files (x86)\Steam\steamapps\common\Homeworld 347380\GBXTools'
)

$ErrorActionPreference = 'Stop'
$vrPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
function Invoke-VrPython {
    & $vrPython @args
    if ($LASTEXITCODE -ne 0) { throw "Python step failed: $args" }
}

Push-Location -LiteralPath $PSScriptRoot
try {
    if (-not (Test-Path -LiteralPath 'local\demo-audit.json')) {
        Invoke-VrPython tools/audit_demo.py (Join-Path $DemoRoot 'HomeworldVastReachesDemo_Data')
    }
    if ($Recover -or -not (Test-Path -LiteralPath 'local\recovered\views.json')) {
        Invoke-VrPython tools/recover_ship_data.py $DemoRoot
    }
    if ($Models) {
        Invoke-VrPython tools/build_fleet.py $DemoRoot (Join-Path $ToolkitRoot 'HODOR\HODOR.exe')
    }
    if ($Catalogue) { Invoke-VrPython tools/export_catalogue.py }
    Invoke-VrPython tools/refresh_model_bounds.py
    Invoke-VrPython tools/prepare_combat_probe.py
    Invoke-VrPython tools/prepare_comparison.py
    Invoke-VrPython tools/prepare_native_door.py
    Invoke-VrPython tools/prepare_gallery.py
    Invoke-VrPython tools/prepare_test_mod.py
    Invoke-VrPython tools/verify_physical_gallery.py
    Invoke-VrPython tools/build_big.py (Join-Path $ToolkitRoot 'WorkshopTool\Archive.exe') local/testmod local/VastReachesDemo.big
} finally {
    Pop-Location
}
