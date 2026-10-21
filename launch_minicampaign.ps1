param(
    [ValidateSet('Training','M1','M4')][string]$Chapter='Training',
    [string]$GameRoot='C:\Program Files (x86)\Steam\steamapps\common\Homeworld',
    [switch]$PrintOnly
)
$ErrorActionPreference='Stop'
if (Get-Process -Name HomeworldRM -ErrorAction SilentlyContinue) { throw 'HomeworldRM is already running.' }
$archive=Join-Path $GameRoot 'HomeworldRM\Data\VastReachesMiniCampaign.big'
if (-not (Test-Path -LiteralPath $archive)) { throw 'Install VastReachesMiniCampaign.big in HomeworldRM\Data first.' }
$exe=Join-Path $GameRoot 'HomeworldRM\Bin\Release\HomeworldRM.exe'
$levels=@{Training='T01_Training'; M1='M01_ProvingGrounds'; M4='M04_LostDestroyer'}
$log=Join-Path $env:TEMP 'HWRM-minicampaign.log'
$arguments=@('-mod','VastReachesMiniCampaign.big','-dlccampaign','HW2Campaign.big','-campaign','VastReachesMiniCampaign','-startinglevel',$levels[$Chapter],'-locale','Russian','-windowed','-w','1280','-h','768','-nomovies','-luatrace',"-logfilename=`"$log`"")
if ($PrintOnly) { Write-Output ($exe+' '+($arguments -join ' ')); return }
# A visible game window is intentional only when this launcher is explicitly run.
Start-Process -FilePath $exe -ArgumentList $arguments -WorkingDirectory (Split-Path $exe)
