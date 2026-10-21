param(
    [string]$GameRoot = 'C:\Program Files (x86)\Steam\steamapps\common\Homeworld',
    [switch]$Scene,
    [switch]$Compare,
    [switch]$Gallery
)

$python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
$launcher = Join-Path $PSScriptRoot 'tools\launch_game.py'
$launchArguments = @($launcher, '--game-root', $GameRoot)
if ($Scene) { $launchArguments += '--scene' }
if ($Compare) { $launchArguments += '--compare' }
if ($Gallery) { $launchArguments += '--gallery' }
& $python @launchArguments
