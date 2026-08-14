[CmdletBinding()]
param(
    [string]$EvidenceRoot = "production\qa\evidence\day7-content-validation-2026-08-14-verified",
    [int]$TimeoutSeconds = 120
)

$ErrorActionPreference = "Stop"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$sdk = Join-Path $repo ".tools\renpy-8.5.3-sdk"
$python = Join-Path $sdk "lib\py3-windows-x86_64\python.exe"
$renpy = Join-Path $sdk "renpy.py"
$evidence = Join-Path $repo $EvidenceRoot
$runRoot = Join-Path $evidence "run-passed"
$appData = Join-Path $runRoot "appdata"
$saveDir = Join-Path $runRoot "saves"

if (-not (Test-Path -LiteralPath $python -PathType Leaf)) { throw "Ren'Py Python not found: $python" }
if (Test-Path -LiteralPath $runRoot) { throw "Passed-run directory already exists; use a new EvidenceRoot to preserve raw evidence: $runRoot" }
New-Item -ItemType Directory -Force -Path $runRoot, (Join-Path $appData "RenPy\tokens"), $saveDir | Out-Null

$env:APPDATA = $appData
$arguments = @($renpy, $repo, "test", "global", "--savedir", $saveDir, "--report-detailed", "--overwrite-screenshots")
$psi = [Diagnostics.ProcessStartInfo]::new()
$psi.FileName = $python
$psi.Arguments = (($arguments | ForEach-Object { '"' + $_.Replace('"', '\"') + '"' }) -join ' ')
$psi.WorkingDirectory = $sdk
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true

$process = [Diagnostics.Process]::new()
$process.StartInfo = $psi
$startedAt = [DateTime]::UtcNow
if (-not $process.Start()) { throw "Failed to start Ren'Py testcase process." }
$stdoutLines = New-Object System.Collections.Generic.List[string]
$stderrLines = New-Object System.Collections.Generic.List[string]
$stdoutTask = $process.StandardOutput.ReadLineAsync()
$stderrTask = $process.StandardError.ReadLineAsync()
$statusLine = $null
$deadline = [DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
while (-not $process.HasExited -and -not $statusLine) {
    if ($stdoutTask.IsCompleted) {
        $line = $stdoutTask.Result
        if ($null -ne $line) {
            $stdoutLines.Add($line)
            if ($line -match "\[rpytest\] Status:") { $statusLine = $line }
            $stdoutTask = $process.StandardOutput.ReadLineAsync()
        }
    }
    if ($stderrTask.IsCompleted) {
        $line = $stderrTask.Result
        if ($null -ne $line) { $stderrLines.Add($line); $stderrTask = $process.StandardError.ReadLineAsync() }
    }
    if ([DateTime]::UtcNow -ge $deadline) { $process.Kill(); $process.WaitForExit(5000) | Out-Null; throw "Ren'Py Day 7 evidence run timed out after $TimeoutSeconds seconds." }
    Start-Sleep -Milliseconds 100
}
if (-not $statusLine -and $process.HasExited) { throw "Ren'Py Day 7 evidence run exited before emitting a terminal testcase status." }
if (-not $process.HasExited) { Start-Sleep -Milliseconds 250; $process.Kill(); $process.WaitForExit(5000) | Out-Null }
while ($stdoutTask.IsCompleted) { $line = $stdoutTask.Result; if ($null -eq $line) { break }; $stdoutLines.Add($line); $stdoutTask = $process.StandardOutput.ReadLineAsync() }
while ($stderrTask.IsCompleted) { $line = $stderrTask.Result; if ($null -eq $line) { break }; $stderrLines.Add($line); $stderrTask = $process.StandardError.ReadLineAsync() }
[IO.File]::WriteAllText((Join-Path $runRoot "stdout.txt"), ($stdoutLines -join [Environment]::NewLine), [Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllText((Join-Path $runRoot "stderr.txt"), ($stderrLines -join [Environment]::NewLine), [Text.UTF8Encoding]::new($false))

$result = [ordered]@{
    engine = "Ren'Py 8.5.3.26051504"
    project = $repo
    day7_source_sha256 = (Get-FileHash -LiteralPath (Join-Path $repo "game\chapters\day7.rpy") -Algorithm SHA256).Hash.ToLowerInvariant()
    testcases_sha256 = (Get-FileHash -LiteralPath (Join-Path $repo "game\testcases.rpy") -Algorithm SHA256).Hash.ToLowerInvariant()
    arguments = $arguments
    started_utc = $startedAt.ToString("o")
    finished_utc = ([DateTime]::UtcNow).ToString("o")
    exit_code = $process.ExitCode
    status_line = $statusLine
    stdout_sha256 = (Get-FileHash -LiteralPath (Join-Path $runRoot "stdout.txt") -Algorithm SHA256).Hash.ToLowerInvariant()
    stderr_sha256 = (Get-FileHash -LiteralPath (Join-Path $runRoot "stderr.txt") -Algorithm SHA256).Hash.ToLowerInvariant()
}
$result | ConvertTo-Json -Depth 8 | Set-Content -Encoding utf8 -LiteralPath (Join-Path $runRoot "result.json")

$captures = @(
    "visual\day7_causal_recall_1280x720_keyboard_silent_reduced_motion.png",
    "visual\day7_causal_recall_1280x720_font_1_5_high_contrast.png"
)
foreach ($relativeCapture in $captures) {
    $sourceCapture = Join-Path $repo (Join-Path "tests\screenshots" $relativeCapture)
    if (-not (Test-Path -LiteralPath $sourceCapture -PathType Leaf)) { throw "Required Day 7 capture was not produced: $sourceCapture" }
    $destinationCapture = Join-Path $runRoot (Join-Path "screenshots" $relativeCapture)
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $destinationCapture) | Out-Null
    Copy-Item -LiteralPath $sourceCapture -Destination $destinationCapture
}

if ($statusLine -notmatch "\[rpytest\] Status: PASSED") { exit 1 }
Write-Host (($stdoutLines -join [Environment]::NewLine).TrimEnd())
