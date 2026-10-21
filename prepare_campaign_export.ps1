$ErrorActionPreference='Stop'
$python=Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
$stages=@('prepare_campaign_localization.py','write_campaign_glossary.py','write_quest_scenarios.py','write_quest_progression.py','prepare_campaign_export.py','prepare_campaign_media.py','write_campaign_reader.py','write_mission_dossiers.py','verify_campaign_export.py','build_campaign_export.py')
foreach ($stage in $stages) {
    & $python -X utf8 (Join-Path $PSScriptRoot ('tools\'+$stage))
    if ($LASTEXITCODE -ne 0) { throw ('Campaign preparation failed: '+$stage) }
}
