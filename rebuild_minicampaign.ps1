$ErrorActionPreference='Stop'
$python=Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
& $python -X utf8 (Join-Path $PSScriptRoot 'tools\prepare_campaign_localization.py')
if ($LASTEXITCODE -ne 0) { throw 'Translation validation failed.' }
& $python -X utf8 (Join-Path $PSScriptRoot 'tools\write_demo_scenarios.py')
if ($LASTEXITCODE -ne 0) { throw 'Reading edition generation failed.' }
& $python -X utf8 (Join-Path $PSScriptRoot 'tools\prepare_minicampaign.py')
if ($LASTEXITCODE -ne 0) { throw 'Campaign generation failed.' }
& $python -X utf8 (Join-Path $PSScriptRoot 'tools\verify_minicampaign.py')
if ($LASTEXITCODE -ne 0) { throw 'Campaign verification failed.' }
& $python -X utf8 (Join-Path $PSScriptRoot 'tools\build_minicampaign.py')
if ($LASTEXITCODE -ne 0) { throw 'Campaign archive build failed.' }
& $python -X utf8 (Join-Path $PSScriptRoot 'tools\package_minicampaign.py')
if ($LASTEXITCODE -ne 0) { throw 'Campaign package creation failed.' }
