[CmdletBinding()]
param(
    [string]$StartDate = (Get-Date).AddDays(1).ToString('yyyy-MM-dd'),
    [int]$Days = 9,
    [int]$PostsPerDay = 1,
    [string]$OutputRoot = 'G:\My Drive\Mo Media Factory\Ready to Post'
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$jobId = "scheduled-revenue-release-$($StartDate.Replace('-', ''))"
$runRoot = Join-Path $OutputRoot $jobId
$receipt = Join-Path $runRoot 'release-receipt.json'
$logRoot = Join-Path $repoRoot 'work\media-ops-logs'
$logPath = Join-Path $logRoot "$jobId.log"
New-Item -ItemType Directory -Force -Path $logRoot | Out-Null

if (Test-Path -LiteralPath $receipt) {
    $existing = Get-Content -LiteralPath $receipt -Raw | ConvertFrom-Json
    if ($existing.status -eq 'READY_TO_POST') {
        "$(Get-Date -Format o) SKIP completed job $jobId" | Add-Content -LiteralPath $logPath
        exit 0
    }
}

Push-Location $repoRoot
try {
    "$(Get-Date -Format o) START $jobId" | Add-Content -LiteralPath $logPath
    & python -m media_ops.runner `
        --config '.\config\brands.json' `
        --numeric-scorecard '.\outputs\media-rebuild-2026-08-10\receipts\campaign-canary-numeric-scorecard.csv' `
        --semantic-scorecard '.\outputs\media-rebuild-2026-08-10\receipts\semantic-provenance-scorecard.csv' `
        --output-root $OutputRoot `
        --start-date $StartDate `
        --days $Days `
        --posts-per-day $PostsPerDay `
        --job-id $jobId *>> $logPath
    if ($LASTEXITCODE -ne 0) {
        throw "Media release runner exited with code $LASTEXITCODE"
    }
    "$(Get-Date -Format o) COMPLETE $jobId" | Add-Content -LiteralPath $logPath
}
finally {
    Pop-Location
}

