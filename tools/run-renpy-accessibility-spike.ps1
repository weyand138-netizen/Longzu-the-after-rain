[CmdletBinding()]
param(
    [string]$EvidenceRoot = "docs\engine-reference\renpy\evidence\2026-08-09-accessibility-spike",
    [string]$FixtureRoot = "",
    [int]$TimeoutSeconds = 120
)

$ErrorActionPreference = "Stop"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$sdk = Join-Path $repo ".tools\renpy-8.5.3-sdk"
$python = Join-Path $sdk "lib\py3-windows-x86_64\python.exe"
$renpy = Join-Path $sdk "renpy.py"
$fixture = if ([string]::IsNullOrWhiteSpace($FixtureRoot)) {
    Join-Path $repo "$EvidenceRoot\fixture"
} else {
    Join-Path $repo $FixtureRoot
}
$evidence = Join-Path $repo $EvidenceRoot
$runRoot = Join-Path $evidence "run"
$appData = Join-Path $runRoot "appdata"
$saveDir = Join-Path $runRoot "saves"

if (-not (Test-Path -LiteralPath $python -PathType Leaf)) { throw "Ren'Py Python not found: $python" }
if (-not (Test-Path -LiteralPath $fixture -PathType Container)) { throw "Accessibility fixture not found: $fixture" }
if (Test-Path -LiteralPath $runRoot) { throw "Run directory already exists; use a new EvidenceRoot to preserve raw evidence: $runRoot" }
New-Item -ItemType Directory -Force -Path $runRoot, (Join-Path $appData "RenPy\tokens"), $saveDir | Out-Null

$env:APPDATA = $appData
$env:RENPY_SKIP_MAIN_MENU = "1"
$arguments = @($renpy, $fixture, "test", "global", "--savedir", $saveDir, "--report-detailed", "--overwrite-screenshots")
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
        if ($null -ne $line) {
            $stderrLines.Add($line)
            $stderrTask = $process.StandardError.ReadLineAsync()
        }
    }
    if ([DateTime]::UtcNow -ge $deadline) {
        $process.Kill()
        $process.WaitForExit(5000) | Out-Null
        throw "Ren'Py accessibility spike timed out after $TimeoutSeconds seconds."
    }
    Start-Sleep -Milliseconds 100
}

# Ren'Py keeps its display loop open after printing the terminal testcase
# report. The report is authoritative, so close the process after capturing it.
if (-not $process.HasExited) {
    Start-Sleep -Milliseconds 250
    $process.Kill()
    $process.WaitForExit(5000) | Out-Null
}

while ($stdoutTask.IsCompleted) {
    $line = $stdoutTask.Result
    if ($null -eq $line) { break }
    $stdoutLines.Add($line)
    $stdoutTask = $process.StandardOutput.ReadLineAsync()
}
while ($stderrTask.IsCompleted) {
    $line = $stderrTask.Result
    if ($null -eq $line) { break }
    $stderrLines.Add($line)
    $stderrTask = $process.StandardError.ReadLineAsync()
}
$stdout = $stdoutLines -join [Environment]::NewLine
$stderr = $stderrLines -join [Environment]::NewLine
$finishedAt = [DateTime]::UtcNow
[IO.File]::WriteAllText((Join-Path $runRoot "stdout.txt"), $stdout, [Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllText((Join-Path $runRoot "stderr.txt"), $stderr, [Text.UTF8Encoding]::new($false))

$result = [ordered]@{
    engine = "Ren'Py 8.5.3.26051504"
    host = [Environment]::OSVersion.VersionString
    python = $python
    fixture = $fixture
    arguments = $arguments
    started_utc = $startedAt.ToString("o")
    finished_utc = $finishedAt.ToString("o")
    duration_ms = [int](($finishedAt - $startedAt).TotalMilliseconds)
    exit_code = $process.ExitCode
    status_line = $statusLine
    stdout_sha256 = (Get-FileHash -LiteralPath (Join-Path $runRoot "stdout.txt") -Algorithm SHA256).Hash.ToLowerInvariant()
    stderr_sha256 = (Get-FileHash -LiteralPath (Join-Path $runRoot "stderr.txt") -Algorithm SHA256).Hash.ToLowerInvariant()
}
$result | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $runRoot "result.json")

# Promote fixture-generated evidence into the preserved run directory. These
# files are produced by the fixture itself; copying them keeps the run
# self-contained without treating debug traces as test results.
$focusLog = Join-Path $fixture "game\focus-log.json"
if (Test-Path -LiteralPath $focusLog -PathType Leaf) {
    Copy-Item -LiteralPath $focusLog -Destination (Join-Path $runRoot "focus-log.json")
}
$transcriptLog = Join-Path $fixture "game\transcript-log.txt"
if (Test-Path -LiteralPath $transcriptLog -PathType Leaf) {
    Copy-Item -LiteralPath $transcriptLog -Destination (Join-Path $runRoot "transcript-log.txt")
}
$viewportLog = Join-Path $fixture "game\viewport-log.json"
if (Test-Path -LiteralPath $viewportLog -PathType Leaf) {
    Copy-Item -LiteralPath $viewportLog -Destination (Join-Path $runRoot "viewport-log.json")
}
$fixtureScreenshots = Join-Path $fixture "tests\screenshots"
if (Test-Path -LiteralPath $fixtureScreenshots -PathType Container) {
    $preservedScreenshots = @(
        "visual\focus_initial_1280x720.png",
        "visual\focus_second_visible_1280x720.png",
        "visual\focus_deep_visible_1280x720.png",
        "visual\layout_1280x720_font_1_5.png",
        "visual\day1_choice_1280x720_keyboard_silent_reduced_motion.png",
        "visual\day1_choice_1280x720_font_1_5_high_contrast.png"
    )
    foreach ($relativeScreenshot in $preservedScreenshots) {
        $sourceScreenshot = Join-Path $fixtureScreenshots $relativeScreenshot
        if (Test-Path -LiteralPath $sourceScreenshot -PathType Leaf) {
            $destinationScreenshot = Join-Path $runRoot (Join-Path "screenshots" $relativeScreenshot)
            New-Item -ItemType Directory -Force -Path (Split-Path -Parent $destinationScreenshot) | Out-Null
            Copy-Item -LiteralPath $sourceScreenshot -Destination $destinationScreenshot
        }
    }
}

$sapi = New-Object -ComObject SAPI.SpVoice
$voices = @($sapi.GetVoices() | ForEach-Object { $_.GetDescription() })
$sapiRecord = [ordered]@{
    checked_utc = [DateTime]::UtcNow.ToString("o")
    com_object_created = $true
    voice_count = $voices.Count
    voice_descriptions = $voices
    note = "Capability enumeration only; no human listening PASS is inferred."
}
$sapiRecord | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $runRoot "sapi-preflight.json")

if ($statusLine -notmatch "\[rpytest\] Status: PASSED") { exit 1 }
Write-Host ($stdout.TrimEnd())
Write-Host ("SAPI voices enumerated: {0}" -f $voices.Count)
