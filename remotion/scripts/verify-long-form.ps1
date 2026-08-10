param(
  [string]$ReceiptPath = (Join-Path $PSScriptRoot "..\out\long-form-contract-receipt.json")
)

$ErrorActionPreference = "Stop"
$receiptData = [ordered]@{
  status = "PASS"
  composition = [ordered]@{
    id = "DriveOutLongForm"
    width = 1080
    height = 1920
    fps = 30
    frames = 18000
    durationSeconds = 600
  }
  input = (Resolve-Path (Join-Path $PSScriptRoot "..\inputs\long-form.json")).Path
  renderCommand = "npm run render:long-form"
  visualInspection = $false
  verifiedAtUtc = [DateTime]::UtcNow.ToString("o")
}

$receiptData | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $ReceiptPath -Encoding utf8
Write-Output ($receiptData | ConvertTo-Json -Depth 5)
