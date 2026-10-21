param(
    [string]$GameRoot,
    [ValidateSet('Russian','English')][string]$Language='Russian',
    [switch]$PrintOnly
)
$ErrorActionPreference='Stop'
if (-not $GameRoot) {
    $relativeGame=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..'))
    if (Test-Path -LiteralPath (Join-Path $relativeGame 'HomeworldRM\Bin\Release\HomeworldRM.exe')) {
        $GameRoot=$relativeGame
    } else {
        $GameRoot='C:\Program Files (x86)\Steam\steamapps\common\Homeworld'
    }
}
$exe=Join-Path $GameRoot 'HomeworldRM\Bin\Release\HomeworldRM.exe'
$archive=Join-Path $GameRoot 'HomeworldRM\DataWorkshopMODs\VastReachesMiniCampaign\VastReachesMiniCampaign.big'
if (-not (Test-Path -LiteralPath $exe)) { throw 'Homeworld Remastered was not found. Supply -GameRoot.' }
if (-not (Test-Path -LiteralPath $archive)) { throw 'Vast Reaches Campaign Demo is not installed.' }
$arguments=@('-workshopmod','"VastReachesMiniCampaign\VastReachesMiniCampaign.big"','-locale',$Language,'-fullscreen')
# Read the primary display rather than reuse the old debug window's 1280x768.
try {
    Add-Type -AssemblyName System.Windows.Forms
    $displayBounds=[System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    if ($displayBounds.Width -ge 800 -and $displayBounds.Height -ge 600) {
        $arguments+=@('-w',[string]$displayBounds.Width,'-h',[string]$displayBounds.Height)
    }
} catch { }
if ($PrintOnly) { Write-Output ($exe+' '+($arguments -join ' ')); return }
if (Get-Process -Name HomeworldRM -ErrorAction SilentlyContinue) { throw 'Homeworld Remastered is already running.' }
# The user explicitly runs this starter to open the normal, visible game menu.
Start-Process -FilePath $exe -ArgumentList $arguments -WorkingDirectory (Split-Path $exe)
