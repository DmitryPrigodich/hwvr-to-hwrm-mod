param(
    [string]$GameRoot = 'C:\Program Files (x86)\Steam\steamapps\common\Homeworld'
)

$source = Join-Path $PSScriptRoot 'local\VastReachesDemo.big'
$destination = Join-Path $GameRoot 'HomeworldRM\Data\VastReachesDemo.big'
$record = Join-Path $PSScriptRoot 'local\installed-mod-sha256.txt'
$sourceHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
if (Test-Path -LiteralPath $destination) {
    $previousHash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash
    if (Test-Path -LiteralPath $record) {
        $expectedHash = (Get-Content -LiteralPath $record -Raw).Trim()
    } else {
        # The first prototype installed during this session.
        $expectedHash = 'F26EE9E8A80CC786791A7F716FA3761E74D8BCDA8328C3893C541F36F7546F3E'
    }
    if ($previousHash -ne $expectedHash) {
        throw 'The installed mod differs from our previous build; refusing to overwrite it.'
    }
    Copy-Item -LiteralPath $destination -Destination (Join-Path $PSScriptRoot 'local\VastReachesDemo.previous.big')
}
Copy-Item -LiteralPath $source -Destination $destination -Force -ErrorAction Stop
$sourceHash | Set-Content -LiteralPath $record -Encoding ascii
Write-Output "Installed VastReachesDemo.big; SHA256=$sourceHash"
