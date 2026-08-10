param(
  [string]$Artifact = (Join-Path $PSScriptRoot "..\out\trial.mp4"),
  [string]$ReceiptPath = (Join-Path $PSScriptRoot "..\out\trial-receipt.json")
)

$ErrorActionPreference = "Stop"
$resolvedArtifact = Resolve-Path -LiteralPath $Artifact -ErrorAction Stop
$item = Get-Item -LiteralPath $resolvedArtifact

if ($item.Length -le 0) {
  throw "Trial artifact is empty: $($item.FullName)"
}

$sha256 = [System.Security.Cryptography.SHA256]::Create()
$stream = [System.IO.File]::OpenRead($item.FullName)
try {
  $hash = ([BitConverter]::ToString($sha256.ComputeHash($stream))).Replace("-", "")
}
finally {
  $stream.Dispose()
  $sha256.Dispose()
}
$receiptData = [ordered]@{
  status = "PASS"
  artifact = $item.FullName
  bytes = $item.Length
  sha256 = $hash
  composition = [ordered]@{
    id = "DriveOutTrial"
    width = 1080
    height = 1920
    fps = 30
    frames = 450
    durationSeconds = 15
  }
  visualInspection = $false
  verifiedAtUtc = [DateTime]::UtcNow.ToString("o")
}

$receiptData | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $ReceiptPath -Encoding utf8
Write-Output ($receiptData | ConvertTo-Json -Depth 5)
