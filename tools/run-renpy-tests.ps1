param(
    [string]$Suite = "global",
    [int]$TimeoutSeconds = 90
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$sdkRoot = Join-Path $projectRoot ".tools\renpy-8.5.3-sdk"
$pythonPath = Join-Path $sdkRoot "lib\py3-windows-x86_64\python.exe"
$renpyPath = Join-Path $sdkRoot "renpy.py"
$runtimeRoot = Join-Path $projectRoot ".renpy"
$appDataPath = Join-Path $runtimeRoot "appdata"
$savePath = Join-Path $runtimeRoot "saves"

if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw "Ren'Py 8.5.3 SDK not found at $sdkRoot"
}

New-Item -ItemType Directory -Force -Path (
    Join-Path $appDataPath "RenPy\tokens"
) | Out-Null
New-Item -ItemType Directory -Force -Path $savePath | Out-Null

$env:APPDATA = $appDataPath

$arguments = @(
    "`"$renpyPath`"",
    "`"$projectRoot`"",
    "test",
    $Suite,
    "--savedir",
    "`"$savePath`"",
    "--report-detailed"
)

$startInfo = New-Object System.Diagnostics.ProcessStartInfo
$startInfo.FileName = $pythonPath
$startInfo.Arguments = $arguments -join " "
$startInfo.WorkingDirectory = $sdkRoot
$startInfo.UseShellExecute = $false
$startInfo.RedirectStandardOutput = $true
$startInfo.RedirectStandardError = $true
$startInfo.CreateNoWindow = $true

$process = $null
$status = $null
$outputLines = New-Object System.Collections.Generic.List[string]
$errorLines = New-Object System.Collections.Generic.List[string]

try {
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $startInfo
    if (-not $process.Start()) {
        throw "Failed to start Ren'Py testcase process."
    }

    $stdoutTask = $process.StandardOutput.ReadLineAsync()
    $stderrTask = $process.StandardError.ReadLineAsync()

    $deadline = [DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
    while (-not $process.HasExited -and -not $status) {
        if ($stdoutTask.IsCompleted) {
            $line = $stdoutTask.Result
            if ($null -ne $line) {
                $outputLines.Add($line)
                if ($line -match "\[rpytest\] Status: (PASSED|FAILED)") {
                    $status = $Matches[1]
                }
                $stdoutTask = $process.StandardOutput.ReadLineAsync()
            }
        }
        if ($stderrTask.IsCompleted) {
            $line = $stderrTask.Result
            if ($null -ne $line) {
                $errorLines.Add($line)
                $stderrTask = $process.StandardError.ReadLineAsync()
            }
        }
        if ([DateTime]::UtcNow -ge $deadline) {
            throw "Ren'Py test report timed out after $TimeoutSeconds seconds."
        }
        Start-Sleep -Milliseconds 100
    }

    if (-not $process.HasExited) {
        # Ren'Py 8.5.3 leaves the display loop open after printing the CLI
        # testcase report. The report is terminal, so close that process tree.
        $process.Kill()
        $process.WaitForExit(5000) | Out-Null
    }

    foreach ($line in $outputLines) {
        Write-Host $line
    }
    if ($errorLines.Count -gt 0) {
        Write-Error ($errorLines -join [Environment]::NewLine)
    }

    if ($status -ne "PASSED") {
        exit 1
    }
    exit 0
}
finally {
    if ($process -and -not $process.HasExited) {
        $process.Kill()
    }
    if ($process) {
        $process.Dispose()
    }
}
