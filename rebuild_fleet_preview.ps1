$ErrorActionPreference='Stop'
$python=Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
& $python -X utf8 (Join-Path $PSScriptRoot 'tools\build_fleet_preview.py')
if ($LASTEXITCODE -ne 0) { throw 'Fleet preview preparation/build failed.' }
Write-Output 'Fleet preview release prepared. Game was not launched.'
