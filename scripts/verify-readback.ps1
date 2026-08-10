param(
  [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot ".."))
)

$ErrorActionPreference = "Stop"
$manifestPath = Join-Path $RepoRoot "docs\READBACK_MANIFEST.json"
$manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json

function Assert-Condition {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) {
    throw "READBACK FAIL: $Message"
  }
}

function Get-Sha256 {
  param([string]$Path)
  $algorithm = [System.Security.Cryptography.SHA256]::Create()
  $stream = [System.IO.File]::OpenRead($Path)
  try {
    return ([BitConverter]::ToString($algorithm.ComputeHash($stream))).Replace("-", "")
  }
  finally {
    $stream.Dispose()
    $algorithm.Dispose()
  }
}

foreach ($relativePath in $manifest.requiredDocumentation) {
  $path = Join-Path $RepoRoot $relativePath
  Assert-Condition (Test-Path -LiteralPath $path -PathType Leaf) "Missing documentation: $relativePath"
}

$artifactResults = @()
foreach ($artifact in $manifest.artifacts) {
  $artifactPath = Join-Path $RepoRoot $artifact.relativePath
  $receiptPath = Join-Path $RepoRoot $artifact.receiptPath
  Assert-Condition (Test-Path -LiteralPath $artifactPath -PathType Leaf) "Missing artifact: $($artifact.relativePath)"
  Assert-Condition (Test-Path -LiteralPath $receiptPath -PathType Leaf) "Missing receipt: $($artifact.receiptPath)"

  $item = Get-Item -LiteralPath $artifactPath
  $receipt = Get-Content -Raw -LiteralPath $receiptPath | ConvertFrom-Json
  $hash = Get-Sha256 -Path $item.FullName

  Assert-Condition ($item.Length -eq [int64]$artifact.bytes) "$($artifact.id) byte count differs from manifest"
  Assert-Condition ($hash -ceq [string]$artifact.sha256) "$($artifact.id) SHA-256 differs from manifest"
  Assert-Condition ($receipt.status -eq "PASS") "$($artifact.id) receipt is not PASS"
  Assert-Condition ([int64]$receipt.bytes -eq $item.Length) "$($artifact.id) receipt byte count differs from artifact"
  Assert-Condition ([string]$receipt.sha256 -ceq $hash) "$($artifact.id) receipt hash differs from artifact"

  $artifactResults += [ordered]@{
    id = $artifact.id
    status = "PASS"
    bytes = $item.Length
    sha256 = $hash
  }
}

$siteVerifier = Join-Path $RepoRoot "scripts\verify-site.ps1"
& powershell -NoProfile -ExecutionPolicy Bypass -File $siteVerifier
Assert-Condition ($LASTEXITCODE -eq 0) "Static-site verifier failed"

Push-Location $RepoRoot
try {
  git diff --exit-code -- LEDGER.md | Out-Null
  Assert-Condition ($LASTEXITCODE -eq 0) "LEDGER.md has a diff"
  $status = git status --porcelain
  Assert-Condition ([string]::IsNullOrWhiteSpace(($status -join "`n"))) "Working tree is not clean"
}
finally {
  Pop-Location
}

[ordered]@{
  status = "PASS"
  evidenceSnapshotCommit = $manifest.evidenceSnapshotCommit
  artifactsChecked = $artifactResults.Count
  artifacts = $artifactResults
  documentationChecked = $manifest.requiredDocumentation.Count
  ledgerUnchanged = $true
  workingTreeClean = $true
  visualInspection = $false
  thirdPartyAssistantAffirmation = "PENDING_INDEPENDENT_REVIEW"
  verifiedAtUtc = [DateTime]::UtcNow.ToString("o")
} | ConvertTo-Json -Depth 6
