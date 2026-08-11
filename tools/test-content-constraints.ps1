param(
    [string]$RepositoryRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = "Stop"

$contentRoots = @(
    (Join-Path $RepositoryRoot "game"),
    (Join-Path $RepositoryRoot "prototypes")
)
$allowedResponse = '^\s*erii\s+"[\u55EF\u5514\u554A\u54E6][\u3002\uFF01\uFF1F\u2026]?"\s*(?:#.*)?$'
$violations = New-Object System.Collections.Generic.List[string]

foreach ($contentRoot in $contentRoots) {
    if (-not (Test-Path -LiteralPath $contentRoot)) {
        continue
    }

    Get-ChildItem -LiteralPath $contentRoot -Recurse -File -Filter "*.rpy" |
        ForEach-Object {
            $file = $_
            Select-String -LiteralPath $file.FullName -Pattern '^\s*erii\s+' |
                ForEach-Object {
                    if ($_.Line -notmatch $allowedResponse) {
                        $relativePath = [IO.Path]::GetRelativePath(
                            $RepositoryRoot,
                            $file.FullName
                        )
                        $violations.Add(
                            "{0}:{1}: {2}" -f
                                $relativePath,
                                $_.LineNumber,
                                $_.Line.Trim()
                        )
                    }
                }
        }
}

if ($violations.Count -gt 0) {
    Write-Error (
        "Erii dialogue constraint failed. Full spoken lines are forbidden:`n" +
        ($violations -join "`n")
    )
    exit 1
}

Write-Host "Erii dialogue constraint passed: only simple monosyllables found."
