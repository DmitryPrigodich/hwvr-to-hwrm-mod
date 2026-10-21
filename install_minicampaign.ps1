param([string]$GameRoot='C:\Program Files (x86)\Steam\steamapps\common\Homeworld')
$ErrorActionPreference='Stop'
$package=Join-Path $PSScriptRoot 'local\VastReachesCampaignDemo-release'
$source=Join-Path $package 'VastReachesMiniCampaign.big'
$gameAbsolute=[IO.Path]::GetFullPath($GameRoot).TrimEnd('\')
$modRoot=[IO.Path]::GetFullPath((Join-Path $gameAbsolute 'HomeworldRM\DataWorkshopMODs'))
$folder=[IO.Path]::GetFullPath((Join-Path $modRoot 'VastReachesMiniCampaign'))
$destination=Join-Path $gameAbsolute 'HomeworldRM\Data\VastReachesMiniCampaign.big'
$record=Join-Path $PSScriptRoot 'local\installed-minicampaign-sha256.txt'
$identity='VastReachesCampaignDemo-release-v1'
if (-not (Test-Path -LiteralPath (Join-Path $gameAbsolute 'HomeworldRM\Bin\Release\HomeworldRM.exe'))) { throw 'HWRM was not found.' }
if ((Split-Path $folder -Parent) -ne $modRoot) { throw 'Unsafe mod destination.' }
if (Get-Process -Name HomeworldRM,Launcher -ErrorAction SilentlyContinue) { throw 'Close HWRM and its launcher before installation.' }
if ((Get-Content -LiteralPath (Join-Path $package 'package-id.txt') -Raw).Trim() -ne $identity) { throw 'Unknown release identity.' }
$hash=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
foreach ($line in (Get-Content -LiteralPath (Join-Path $package 'SHA256SUMS.txt'))) {
    $pair=$line -split '  ',2
    if ($pair.Count -ne 2 -or [IO.Path]::IsPathRooted($pair[1]) -or $pair[1] -match '(^|[\\/])\.\.([\\/]|$)') { throw 'Invalid release manifest.' }
    $releaseFile=[IO.Path]::GetFullPath((Join-Path $package $pair[1]))
    if (-not $releaseFile.StartsWith(([IO.Path]::GetFullPath($package).TrimEnd('\')+'\'),[StringComparison]::OrdinalIgnoreCase)) { throw 'Release path escapes package.' }
    if ((Get-FileHash -LiteralPath $releaseFile -Algorithm SHA256).Hash -ne $pair[0]) { throw 'Release hash mismatch.' }
}
$backupRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'local\install-backups'))
$moviePackage=Join-Path $package 'Movies'
if (Test-Path -LiteralPath $moviePackage) {
    $movieIdentity='VRC-rendered-campaign-movies-v1'
    if ((Get-Content -LiteralPath (Join-Path $moviePackage 'vre-movies-id.txt') -Raw).Trim() -ne $movieIdentity) { throw 'Unknown movie package.' }
    $movieRoot=[IO.Path]::GetFullPath((Join-Path $gameAbsolute 'HomeworldRM\Data\Animatics'))
    $movieFolder=[IO.Path]::GetFullPath((Join-Path $movieRoot 'VastReaches'))
    if ((Split-Path $movieFolder -Parent) -ne $movieRoot) { throw 'Unsafe movie destination.' }
    if (Test-Path -LiteralPath $movieFolder) {
        if ((Get-Content -LiteralPath (Join-Path $movieFolder 'vre-movies-id.txt') -Raw).Trim() -ne $movieIdentity) { throw 'Unknown installed movie folder.' }
    }
}
if (Test-Path -LiteralPath $destination) {
    $previous=(Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash
    if ($previous -ne $hash) {
        if (-not (Test-Path -LiteralPath $record)) { throw 'Unknown installed archive.' }
        if ($previous -ne (Get-Content -LiteralPath $record -Raw).Trim()) { throw 'Installed archive has outside edits.' }
        Copy-Item -LiteralPath $destination -Destination (Join-Path $PSScriptRoot 'local\VastReachesMiniCampaign.previous.big')
    }
}
if (Test-Path -LiteralPath $folder) {
    $oldMarker=Join-Path $folder 'package-id.txt'
    if (-not (Test-Path -LiteralPath $oldMarker)) { throw 'Unknown installed folder.' }
    $oldIdentity=(Get-Content -LiteralPath $oldMarker -Raw).Trim()
    if ($oldIdentity -notin @('VastReachesMiniCampaign-local-script-prototype',$identity)) { throw 'Unknown installed package identity.' }
    # Preserve the whole previous package, including any user edits, outside the game.
    $backupRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'local\install-backups'))
    New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
    $backupIndex=1
    do {
        $backup=[IO.Path]::GetFullPath((Join-Path $backupRoot ('previous-installed-package-'+$backupIndex)))
        $backupIndex++
    } while (Test-Path -LiteralPath $backup)
    if ((Split-Path $backup -Parent) -ne $backupRoot) { throw 'Unsafe backup destination.' }
    if ($folder -ne (Join-Path $modRoot 'VastReachesMiniCampaign')) { throw 'Unsafe source for package move.' }
    Move-Item -LiteralPath $folder -Destination $backup
    Write-Output "Previous working package preserved outside game: $backup"
}
New-Item -ItemType Directory -Path $folder | Out-Null
Get-ChildItem -LiteralPath $package -File | Copy-Item -Destination $folder -Force
$moviePackage=Join-Path $package 'Movies'
if (Test-Path -LiteralPath $moviePackage) {
    $movieIdentity='VRC-rendered-campaign-movies-v1'
    if ((Get-Content -LiteralPath (Join-Path $moviePackage 'vre-movies-id.txt') -Raw).Trim() -ne $movieIdentity) { throw 'Unknown movie package.' }
    $movieRoot=[IO.Path]::GetFullPath((Join-Path $gameAbsolute 'HomeworldRM\Data\Animatics'))
    $movieFolder=[IO.Path]::GetFullPath((Join-Path $movieRoot 'VastReaches'))
    if ((Split-Path $movieFolder -Parent) -ne $movieRoot) { throw 'Unsafe movie destination.' }
    if (Test-Path -LiteralPath $movieFolder) {
        if ((Get-Content -LiteralPath (Join-Path $movieFolder 'vre-movies-id.txt') -Raw).Trim() -ne $movieIdentity) { throw 'Unknown installed movie folder.' }
        $movieBackupIndex=1
        do {
            $movieBackup=[IO.Path]::GetFullPath((Join-Path $backupRoot ('previous-installed-movies-'+$movieBackupIndex)))
            $movieBackupIndex++
        } while (Test-Path -LiteralPath $movieBackup)
        if ((Split-Path $movieBackup -Parent) -ne $backupRoot) { throw 'Unsafe movie backup.' }
        Move-Item -LiteralPath $movieFolder -Destination $movieBackup
    }
    Copy-Item -LiteralPath $moviePackage -Destination (Join-Path $folder 'Movies') -Recurse
    New-Item -ItemType Directory -Path $movieRoot -Force | Out-Null
    Copy-Item -LiteralPath $moviePackage -Destination $movieFolder -Recurse
    foreach ($movieFile in (Get-ChildItem -LiteralPath $moviePackage -File -Recurse)) {
        $movieRelative=$movieFile.FullName.Substring($moviePackage.TrimEnd('\').Length+1)
        $movieHash=(Get-FileHash -LiteralPath $movieFile.FullName -Algorithm SHA256).Hash
        if ((Get-FileHash -LiteralPath (Join-Path $movieFolder $movieRelative) -Algorithm SHA256).Hash -ne $movieHash) { throw 'Installed movie hash mismatch.' }
    }
}
Copy-Item -LiteralPath $source -Destination $destination -Force
if ((Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash -ne $hash) { throw 'Installed archive hash mismatch.' }
$hash | Set-Content -LiteralPath $record -Encoding ascii
$python=Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
$tool=Join-Path $PSScriptRoot 'tools\register_launcher_mod.py'
& $python -X utf8 $tool prepare | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'Launcher payload preparation failed.' }
$slotState=Join-Path $PSScriptRoot 'local\launcher-mod-registration\slot-backup.json'
if (Test-Path -LiteralPath $slotState) {
    $registration=Get-Content -LiteralPath $slotState -Raw | ConvertFrom-Json
    if ($registration.phase -eq 'installed') {
        & $python -X utf8 $tool install | Out-Null
        if ($LASTEXITCODE -ne 0) { throw 'Launcher slot update failed.' }
    }
}
Write-Output "Installed release: $folder"
Write-Output "SHA256: $hash"
Write-Output 'In game: Extra Missions > Vast Reaches Campaign Demo. Game was not launched.'
