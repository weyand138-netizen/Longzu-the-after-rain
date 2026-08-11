[CmdletBinding()]
param(
    [string]$RepoRoot = ".",
    [string]$EvidenceRoot = "docs\engine-reference\renpy\evidence\2026-08-09-build-q1-spike"
)

$ErrorActionPreference = "Stop"
[void][Reflection.Assembly]::LoadWithPartialName("System.IO.Compression.FileSystem")
if ($RepoRoot -eq ".") {
    $RepoRoot = Split-Path -Parent $PSScriptRoot
}
$repo = (Resolve-Path $RepoRoot).Path
$evidence = Join-Path $repo $EvidenceRoot
$sdk = Join-Path $repo ".tools\renpy-8.5.3-sdk"
$renpyExe = Join-Path $sdk "renpy.exe"

if (-not (Test-Path $renpyExe -PathType Leaf)) {
    throw "Ren'Py executable not found: $renpyExe"
}
if (Test-Path $evidence) {
    throw "Evidence directory already exists. Choose a new EvidenceRoot to avoid overwriting raw evidence: $evidence"
}

New-Item -ItemType Directory -Force -Path $evidence | Out-Null
$fixtures = Join-Path $evidence "fixtures"
$cases = Join-Path $evidence "cases"
New-Item -ItemType Directory -Force -Path $fixtures, $cases | Out-Null

function Write-Utf8NoBom([string]$Path, [string]$Content) {
    $parent = Split-Path -Parent $Path
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
    [IO.File]::WriteAllText($Path, $Content, [Text.UTF8Encoding]::new($false))
}

function ConvertTo-ProcessArgument([string]$Argument) {
    return '"' + $Argument.Replace('"', '\"') + '"'
}

function New-Fixture([string]$Name, [string]$Mode) {
    $root = Join-Path $fixtures $Name
    $game = Join-Path $root "game"
    New-Item -ItemType Directory -Force -Path $game | Out-Null

    $options = @'
define config.name = "RenPy Build Spike"
define config.version = "0.0.1"
define config.window_title = "RenPy Build Spike"

init python:
    build.name = "renpy-build-spike"
    build.directory_name = "renpy-build-spike-0.0.1"
    build.executable_name = "renpy-build-spike"
    build.package("win", "zip", "windows renpy all")
'@
    if ($Mode -eq "slow") {
        $options += @'

init python:
    import time
    time.sleep(30)
'@
    }

    Write-Utf8NoBom (Join-Path $game "options.rpy") $options
    Write-Utf8NoBom (Join-Path $game "script.rpy") @'
label start:
    "Build spike fixture."
    return
'@
    Write-Utf8NoBom (Join-Path $root "README.md") "Ren'Py 8.5.3 build spike fixture.`n"

    if ($Mode -eq "lint-failure") {
        Write-Utf8NoBom (Join-Path $game "broken.rpy") @'
label broken
    "This statement is intentionally malformed"
'@
    }
    return $root
}

function Get-ProcessSnapshot {
    try {
        @(Get-CimInstance Win32_Process -ErrorAction Stop |
            Where-Object {
                $_.ExecutablePath -eq $renpyExe -or
                $_.CommandLine -like "*$($sdk.Replace('\', '\'))*"
            } |
            Select-Object ProcessId, ParentProcessId, Name, ExecutablePath, CommandLine)
    } catch {
        @()
    }
}

function Get-DescendantProcessIds([int]$RootProcessId) {
    try {
        $all = @(Get-CimInstance Win32_Process -ErrorAction Stop)
        $pending = @($RootProcessId)
        $found = @()
        while ($pending.Count -gt 0) {
            $parent = $pending[0]
            if ($pending.Count -eq 1) { $pending = @() } else { $pending = @($pending[1..($pending.Count - 1)]) }
            $children = @($all | Where-Object { [int]$_.ParentProcessId -eq $parent })
            foreach ($child in $children) {
                $childId = [int]$child.ProcessId
                if ($found -notcontains $childId) {
                    $found += $childId
                    $pending += $childId
                }
            }
        }
        return $found
    } catch {
        return @()
    }
}

function Stop-ProcessTree([Diagnostics.Process]$Process, [int]$RootProcessId) {
    $descendants = @(Get-DescendantProcessIds $RootProcessId)
    foreach ($childId in ($descendants | Sort-Object -Descending)) {
        Stop-Process -Id $childId -Force -ErrorAction SilentlyContinue
    }
    try {
        $Process.Kill()
    } catch {
        Stop-Process -Id $RootProcessId -Force -ErrorAction SilentlyContinue
    }
    foreach ($childId in ($descendants | Sort-Object -Descending)) {
        Stop-Process -Id $childId -Force -ErrorAction SilentlyContinue
    }
}

function Get-TreeText([string]$Path) {
    if (-not (Test-Path $Path)) {
        return "<absent>"
    }
    $items = @(Get-ChildItem -LiteralPath $Path -Recurse -Force -File -ErrorAction SilentlyContinue |
        ForEach-Object {
            $relative = $_.FullName.Substring($Path.Length).TrimStart('\', '/')
            $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            "{0}`t{1}`t{2}`t{3}" -f $relative, $_.Length, $_.LastWriteTimeUtc.ToString("o"), $hash
        })
    if ($items.Count -eq 0) { return "<empty>" }
    return ($items | Sort-Object) -join "`n"
}

function Get-ZipInventory([string]$CaseDir, [string]$ArtifactRoot) {
    $zips = @(Get-ChildItem -LiteralPath $ArtifactRoot -Recurse -File -Filter *.zip -ErrorAction SilentlyContinue)
    foreach ($zip in $zips) {
        $rows = @()
        $archive = [IO.Compression.ZipFile]::OpenRead($zip.FullName)
        try {
            foreach ($entry in ($archive.Entries | Sort-Object FullName)) {
                $rows += "{0}`t{1}`t{2}" -f $entry.FullName, $entry.Length, $entry.CompressedLength
            }
        } finally {
            $archive.Dispose()
        }
        $out = Join-Path $CaseDir ($zip.BaseName + ".zip-list.txt")
        Write-Utf8NoBom $out (($rows -join "`n") + "`n")
    }
}

function Run-Case(
    [string]$Name,
    [string[]]$Arguments,
    [string]$Fixture,
    [int]$TimeoutMs = 120000,
    [int]$TerminateAfterMs = 0,
    [string]$TerminationKind = "none"
) {
    $caseDir = Join-Path $cases $Name
    $artifactRoot = Join-Path $caseDir "artifacts"
    $logRoot = Join-Path $caseDir "logs"
    New-Item -ItemType Directory -Force -Path $caseDir, $artifactRoot, $logRoot | Out-Null

    $sdkFixtureTemp = Join-Path $sdk "tmp\$Fixture"
    if (Test-Path $sdkFixtureTemp) {
        Remove-Item -LiteralPath $sdkFixtureTemp -Recurse -Force
    }

    $appData = Join-Path $caseDir "appdata"
    New-Item -ItemType Directory -Force -Path (Join-Path $appData "RenPy\tokens") | Out-Null
    $fixtureRoot = Join-Path $fixtures $Fixture
    $envMap = @{
        APPDATA = $appData
        RENPY_LOG_BASE = $logRoot
    }

    $commandText = @(
        "executable=$renpyExe"
        "working_directory=$sdk"
        "arguments=$($Arguments -join ' | ')"
        "fixture=$fixtureRoot"
        "timeout_ms=$TimeoutMs"
        "termination_after_ms=$TerminateAfterMs"
        "termination_kind=$TerminationKind"
        "environment.APPDATA=$appData"
        "environment.RENPY_LOG_BASE=$logRoot"
    ) -join "`n"
    Write-Utf8NoBom (Join-Path $caseDir "command.txt") ($commandText + "`n")
    Write-Utf8NoBom (Join-Path $caseDir "fixture-tree.txt") (Get-TreeText $fixtureRoot)
    Write-Utf8NoBom (Join-Path $caseDir "output-tree-before.txt") (Get-TreeText $artifactRoot)
    Write-Utf8NoBom (Join-Path $caseDir "sdk-tmp-before.txt") (Get-TreeText (Join-Path $sdk "tmp"))

    $beforeProcesses = @(Get-ProcessSnapshot)
    $psi = [Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $renpyExe
    $psi.WorkingDirectory = $sdk
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.Arguments = (($Arguments | ForEach-Object { ConvertTo-ProcessArgument $_ }) -join " ")
    $oldAppData = $env:APPDATA
    $oldRenpyLogBase = $env:RENPY_LOG_BASE
    $env:APPDATA = $appData
    $env:RENPY_LOG_BASE = $logRoot

    $proc = [Diagnostics.Process]::new()
    $proc.StartInfo = $psi
    $startedAt = [DateTime]::UtcNow
    $started = $proc.Start()
    $env:APPDATA = $oldAppData
    $env:RENPY_LOG_BASE = $oldRenpyLogBase
    if (-not $started) { throw "Unable to start $renpyExe" }
    $processId = $proc.Id
    $stdoutTask = $proc.StandardOutput.ReadToEndAsync()
    $stderrTask = $proc.StandardError.ReadToEndAsync()
    $timedOut = $false
    $terminated = $false
    $terminationObservedAt = $null

    if ($TerminateAfterMs -gt 0) {
        Start-Sleep -Milliseconds $TerminateAfterMs
        if (-not $proc.HasExited) {
            $terminated = $true
            $terminationObservedAt = [DateTime]::UtcNow
            Stop-ProcessTree $proc $processId
            $proc.WaitForExit()
        }
    } else {
        if (-not $proc.WaitForExit($TimeoutMs)) {
            $timedOut = $true
            $terminationObservedAt = [DateTime]::UtcNow
            Stop-ProcessTree $proc $processId
            $proc.WaitForExit()
        }
    }

    $stdout = $stdoutTask.GetAwaiter().GetResult()
    $stderr = $stderrTask.GetAwaiter().GetResult()
    $finishedAt = [DateTime]::UtcNow
    $exitCode = $proc.ExitCode
    $afterProcesses = @(Get-ProcessSnapshot)

    Write-Utf8NoBom (Join-Path $caseDir "stdout.txt") $stdout
    Write-Utf8NoBom (Join-Path $caseDir "stderr.txt") $stderr
    Write-Utf8NoBom (Join-Path $caseDir "output-tree-after.txt") (Get-TreeText $artifactRoot)
    Write-Utf8NoBom (Join-Path $caseDir "sdk-tmp-after.txt") (Get-TreeText (Join-Path $sdk "tmp"))
    if ($afterProcesses.Count -eq 0) {
        Write-Utf8NoBom (Join-Path $caseDir "processes-after.txt") "<no matching Ren'Py processes> `n"
    } else {
        Write-Utf8NoBom (Join-Path $caseDir "processes-after.txt") (($afterProcesses | Format-List | Out-String).TrimEnd() + "`n")
    }
    Copy-Item -LiteralPath (Join-Path $sdk "tmp\$Fixture\distribute.txt") -Destination (Join-Path $caseDir "distribute.txt") -Force -ErrorAction SilentlyContinue
    Get-ZipInventory $caseDir $artifactRoot

    $result = [ordered]@{
        name = $Name
        fixture = $Fixture
        executable = $renpyExe
        working_directory = $sdk
        arguments = $Arguments
        timeout_ms = $TimeoutMs
        termination_after_ms = $TerminateAfterMs
        termination_kind = $TerminationKind
        started_utc = $startedAt.ToString("o")
        finished_utc = $finishedAt.ToString("o")
        duration_ms = [int](($finishedAt - $startedAt).TotalMilliseconds)
        pid = $processId
        process_exit_code = $exitCode
        timed_out = $timedOut
        externally_terminated = $terminated
        termination_observed_utc = if ($terminationObservedAt) { $terminationObservedAt.ToString("o") } else { $null }
        stdout_bytes = [Text.Encoding]::UTF8.GetByteCount($stdout)
        stderr_bytes = [Text.Encoding]::UTF8.GetByteCount($stderr)
        log_files = @(Get-ChildItem -LiteralPath $logRoot -File -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name)
        output_file_count = @(Get-ChildItem -LiteralPath $artifactRoot -Recurse -File -ErrorAction SilentlyContinue).Count
        sdk_tmp_fixture_exists = Test-Path (Join-Path $sdk "tmp\$Fixture")
        matching_processes_before = @($beforeProcesses | Select-Object -ExpandProperty ProcessId)
        matching_processes_after = @($afterProcesses | Select-Object -ExpandProperty ProcessId)
    }
    $json = $result | ConvertTo-Json -Depth 8
    Write-Utf8NoBom (Join-Path $caseDir "result.json") ($json + "`n")
}

function Run-Probe([string]$Name, [string[]]$Arguments) {
    $caseDir = Join-Path $evidence "cli-probes\$Name"
    $logRoot = Join-Path $caseDir "logs"
    $appData = Join-Path $caseDir "appdata"
    New-Item -ItemType Directory -Force -Path $caseDir, $logRoot, (Join-Path $appData "RenPy\tokens") | Out-Null
    Write-Utf8NoBom (Join-Path $caseDir "command.txt") @(
        "executable=$renpyExe"
        "working_directory=$sdk"
        "arguments=$($Arguments -join ' | ')"
        "environment.APPDATA=$appData"
        "environment.RENPY_LOG_BASE=$logRoot"
    )

    $psi = [Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $renpyExe
    $psi.WorkingDirectory = $sdk
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.Arguments = (($Arguments | ForEach-Object { ConvertTo-ProcessArgument $_ }) -join " ")
    $oldAppData = $env:APPDATA
    $oldRenpyLogBase = $env:RENPY_LOG_BASE
    $env:APPDATA = $appData
    $env:RENPY_LOG_BASE = $logRoot
    $p = [Diagnostics.Process]::new()
    $p.StartInfo = $psi
    $null = $p.Start()
    $env:APPDATA = $oldAppData
    $env:RENPY_LOG_BASE = $oldRenpyLogBase
    $outTask = $p.StandardOutput.ReadToEndAsync()
    $errTask = $p.StandardError.ReadToEndAsync()
    $p.WaitForExit()
    Write-Utf8NoBom (Join-Path $caseDir "stdout.txt") $outTask.GetAwaiter().GetResult()
    Write-Utf8NoBom (Join-Path $caseDir "stderr.txt") $errTask.GetAwaiter().GetResult()
    Write-Utf8NoBom (Join-Path $caseDir "result.txt") ("process_exit_code=$($p.ExitCode)`n")
}

Run-Probe "version" @("--version")
Run-Probe "distribute-help" @("launcher", "distribute", "--help")

$success = New-Fixture "success" "success"
$lintFailure = New-Fixture "lint-failure" "lint-failure"
$buildFailure = New-Fixture "build-failure" "success"
$interrupt = New-Fixture "interrupt" "slow"
$timeout = New-Fixture "timeout" "slow"

Run-Case "lint-success" @($success, "lint", "--compile") "success"
Run-Case "build-success" @("launcher", "distribute", "--destination", (Join-Path $cases "build-success\artifacts"), "--package", "win", "--format", "zip", "--no-update", $success) "success"
Run-Case "lint-failure" @($lintFailure, "lint") "lint-failure"
Run-Case "build-failure-invalid-format" @("launcher", "distribute", "--destination", (Join-Path $cases "build-failure-invalid-format\artifacts"), "--package", "win", "--format", "not-a-real-format", "--no-update", $buildFailure) "build-failure"
Run-Case "interrupted" @("launcher", "distribute", "--destination", (Join-Path $cases "interrupted\artifacts"), "--package", "win", "--format", "zip", "--no-update", $interrupt) "interrupt" 120000 1500 "external-process-kill"
Run-Case "timeout" @("launcher", "distribute", "--destination", (Join-Path $cases "timeout\artifacts"), "--package", "win", "--format", "zip", "--no-update", $timeout) "timeout" 2500 0 "timeout-kill"

$fixtureSnapshot = Get-TreeText $fixtures
Write-Utf8NoBom (Join-Path $evidence "fixture-tree.txt") ($fixtureSnapshot + "`n")
Write-Utf8NoBom (Join-Path $evidence "sdk-version.txt") ((& $renpyExe --version 2>&1 | Out-String).TrimEnd() + "`n")
Write-Utf8NoBom (Join-Path $evidence "README.txt") @"
SYS-BUILD Ren'Py 8.5.3 Windows build capability spike
Date: 2026-08-09
Runner: $renpyExe
Build CLI: renpy.exe launcher distribute [options] <project>
SDK working directory: $sdk
Evidence is raw process output plus filesystem/process snapshots. Binary packages are retained only under the case artifact folders; the text evidence records their hashes and zip member lists.
Termination cases use Process.Kill(entireProcessTree=true): external-process-kill models interruption; timeout-kill models a timeout supervisor.
"@
