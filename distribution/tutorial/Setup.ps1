param(
    [string]$GameRoot,
    [string]$BackupRoot,
    [ValidateSet('Russian','English')][string]$Language='Russian',
    [switch]$Launch,
    [switch]$Fullscreen,
    [switch]$PlanOnly,
    [switch]$VerifyOnly
)
$ErrorActionPreference='Stop'
function Get-Sha256([string]$file) {
    $stream=[IO.File]::OpenRead($file)
    $hasher=[Security.Cryptography.SHA256]::Create()
    try { return [BitConverter]::ToString($hasher.ComputeHash($stream)).Replace('-','') }
    finally { $hasher.Dispose(); $stream.Dispose() }
}
$identity='VRC-tutorial-showcase-v1'
$package=[IO.Path]::GetFullPath($PSScriptRoot).TrimEnd('\')
$payload=Join-Path $package 'payload'
if ((Get-Content -LiteralPath (Join-Path $payload 'showcase-id.txt') -Raw).Trim() -ne $identity) { throw 'Unknown tutorial package.' }
foreach ($line in (Get-Content -LiteralPath (Join-Path $package 'SHA256SUMS.txt'))) {
    $pair=$line -split '  ',2
    if ($pair.Count -ne 2 -or [IO.Path]::IsPathRooted($pair[1]) -or $pair[1] -match '(^|[\\/])\.\.([\\/]|$)') { throw 'Invalid package manifest.' }
    $file=[IO.Path]::GetFullPath((Join-Path $package $pair[1]))
    if (-not $file.StartsWith($package+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Package path escapes its folder.' }
    if ((Get-Sha256 $file) -ne $pair[0]) { throw ('Damaged package file: '+$pair[1]) }
}
if ($VerifyOnly) { Write-Output 'Package checksums: OK'; return }

function Test-GameRoot([string]$candidate) {
    return $candidate -and (Test-Path -LiteralPath (Join-Path $candidate 'HomeworldRM\Bin\Release\HomeworldRM.exe'))
}
if (-not $GameRoot) {
    $candidates=@([IO.Path]::GetFullPath((Join-Path $package '..\..\..')))
    $steamRoots=@(${env:ProgramFiles(x86)}+'\Steam')
    foreach ($key in @('HKCU:\Software\Valve\Steam','HKLM:\SOFTWARE\WOW6432Node\Valve\Steam')) {
        if (Test-Path -LiteralPath $key) {
            $settings=Get-ItemProperty -LiteralPath $key
            if ($settings.SteamPath) { $steamRoots+=$settings.SteamPath }
            if ($settings.InstallPath) { $steamRoots+=$settings.InstallPath }
        }
    }
    foreach ($steam in ($steamRoots | Select-Object -Unique)) {
        $candidates+=Join-Path $steam 'steamapps\common\Homeworld'
        $libraries=Join-Path $steam 'steamapps\libraryfolders.vdf'
        if (Test-Path -LiteralPath $libraries) {
            foreach ($match in [regex]::Matches((Get-Content -LiteralPath $libraries -Raw),'"path"\s+"([^"]+)"')) {
                $library=$match.Groups[1].Value.Replace('\\','\')
                $candidates+=Join-Path $library 'steamapps\common\Homeworld'
            }
        }
    }
    $GameRoot=$candidates | Where-Object { Test-GameRoot $_ } | Select-Object -First 1
    if (-not $GameRoot) {
        if ($PlanOnly) { throw 'Supply -GameRoot pointing to your Homeworld folder.' }
        $GameRoot=(Read-Host 'Path to Homeworld (the folder containing HomeworldRM)').Trim('"')
    }
}
if (-not (Test-GameRoot $GameRoot)) { throw 'Homeworld Remastered was not found in that folder.' }
$game=[IO.Path]::GetFullPath($GameRoot).TrimEnd('\')
$modParent=[IO.Path]::GetFullPath((Join-Path $game 'HomeworldRM\DataWorkshopMODs'))
$movieParent=[IO.Path]::GetFullPath((Join-Path $game 'HomeworldRM\Data\Animatics'))
$mod=[IO.Path]::GetFullPath((Join-Path $modParent 'VastReachesTutorial'))
$movies=[IO.Path]::GetFullPath((Join-Path $movieParent 'VastReachesTutorial'))
if ((Split-Path $mod -Parent) -ne $modParent -or (Split-Path $movies -Parent) -ne $movieParent) { throw 'Unsafe installation path.' }
$gameArgs=@('-workshopmod','VastReachesTutorial\VastReachesTutorial.big','-locale',$Language)
if ($Fullscreen) { $gameArgs+='-fullscreen' } else { $gameArgs+=@('-windowed','-w','1600','-h','900') }
if ($PlanOnly) {
    [pscustomobject]@{GameRoot=$game;Mod=$mod;Movies=$movies;Arguments=$gameArgs;Launch=[bool]$Launch} | ConvertTo-Json
    return
}
foreach ($process in (Get-Process -Name HomeworldRM,Launcher -ErrorAction SilentlyContinue)) {
    $processPath=$null
    try { $processPath=$process.Path } catch { }
    if (-not $processPath -or $processPath.StartsWith($game+'\',[StringComparison]::OrdinalIgnoreCase)) {
        throw 'Close Homeworld Remastered and its launcher first.'
    }
}
foreach ($folder in @($mod,$movies)) {
    if (Test-Path -LiteralPath $folder) {
        $marker=Join-Path $folder 'showcase-id.txt'
        if (-not (Test-Path -LiteralPath $marker) -or (Get-Content -LiteralPath $marker -Raw).Trim() -ne $identity) {
            throw ('An unrecognized folder already exists: '+$folder)
        }
    }
}
function Test-InstalledFiles {
    foreach ($source in (Get-ChildItem -LiteralPath $payload -File -Recurse)) {
        $relative=$source.FullName.Substring($payload.TrimEnd('\').Length+1)
        if ($relative.StartsWith('Movies\')) { $target=Join-Path $movies $relative.Substring(7) }
        else { $target=Join-Path $mod $relative }
        if (-not (Test-Path -LiteralPath $target)) { return $false }
        if ((Get-Sha256 $source.FullName) -ne (Get-Sha256 $target)) { return $false }
    }
    return $true
}
if (-not (Test-InstalledFiles)) {
    if ($BackupRoot) { $backupRoot=[IO.Path]::GetFullPath($BackupRoot) }
    else { $backupRoot=[IO.Path]::GetFullPath((Join-Path $env:LOCALAPPDATA 'VastReachesTutorial\backups')) }
    if ($backupRoot.StartsWith($game+'\',[StringComparison]::OrdinalIgnoreCase) -or $backupRoot -eq $game) { throw 'Backups must be outside the game folder.' }
    $backup=[IO.Path]::GetFullPath((Join-Path $backupRoot ([DateTime]::Now.ToString('yyyyMMdd-HHmmss')+'-'+[Guid]::NewGuid().ToString('N'))))
    if ((Split-Path $backup -Parent) -ne $backupRoot) { throw 'Unsafe backup path.' }
    foreach ($folder in @($mod,$movies)) {
        if (Test-Path -LiteralPath $folder) {
            New-Item -ItemType Directory -Path $backup -Force | Out-Null
            $name=if ($folder -eq $mod) { 'Mod' } else { 'Movies' }
            Move-Item -LiteralPath $folder -Destination (Join-Path $backup $name)
        }
    }
    New-Item -ItemType Directory -Path $mod -Force | Out-Null
    New-Item -ItemType Directory -Path $movieParent -Force | Out-Null
    Get-ChildItem -LiteralPath $payload -File | Copy-Item -Destination $mod -Force
    Copy-Item -LiteralPath (Join-Path $payload 'Movies') -Destination $movies -Recurse
    if (-not (Test-InstalledFiles)) { throw 'Installed files failed checksum verification.' }
}
Write-Output 'Vast Reaches Tutorial installed. Extra Missions -> Vast Reaches: Tutorial -> M0.'
if ($Launch) {
    $exe=Join-Path $game 'HomeworldRM\Bin\Release\HomeworldRM.exe'
    Start-Process -FilePath $exe -ArgumentList $gameArgs -WorkingDirectory (Split-Path $exe) -WindowStyle Normal
}
