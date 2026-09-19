param(
    [string]$RepositoryRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = "Stop"

$sourcePath = Join-Path $RepositoryRoot "game\chapters\day5.rpy"
$modulePath = Join-Path $RepositoryRoot "game\modules\day5_source_generation.py"
$hash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
$module = @"
`"`"`"Generated Day 5 authored-source generation identifier.`"`"`"

DAY5_SOURCE_SHA256 = `"$hash`"
"@
[System.IO.File]::WriteAllText(
    $modulePath,
    $module,
    (New-Object System.Text.UTF8Encoding($false))
)
Write-Host $hash
