param([string]$GameRoot='C:\Program Files (x86)\Steam\steamapps\common\Homeworld',[switch]$PrintOnly)
$ErrorActionPreference='Stop'
$exe=Join-Path $GameRoot 'HWLauncher\Launcher.exe'
if (-not (Test-Path -LiteralPath $exe)) { throw 'Official HWLauncher not found.' }
$arguments='-locale Russian -fullscreen'
if ($PrintOnly) { Write-Output ($exe+' '+$arguments); return }
if (Get-Process -Name Launcher,HomeworldRM -ErrorAction SilentlyContinue) { throw 'Close the current launcher/game first.' }
# Running this starter explicitly requests the interactive official mod menu.
Start-Process -FilePath $exe -ArgumentList $arguments -WorkingDirectory (Split-Path $exe)
