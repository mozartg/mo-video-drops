$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$inputRoot = Join-Path $root "inputs\drops"
$outputRoot = Join-Path $root "out\drops"
New-Item -ItemType Directory -Force -Path $outputRoot | Out-Null

$inputs = Get-ChildItem -LiteralPath $inputRoot -Filter "drop-*.json" | Sort-Object Name
if ($inputs.Count -ne 5) {
  throw "Expected exactly five drop inputs, found $($inputs.Count)"
}

foreach ($input in $inputs) {
  $name = [System.IO.Path]::GetFileNameWithoutExtension($input.Name)
  $artifact = Join-Path $outputRoot "$name.mp4"
  $receipt = Join-Path $outputRoot "$name-receipt.json"
  Write-Output "Rendering $name"
  & npx remotion render src/index.ts DriveOutTrial $artifact ("--props=" + $input.FullName) --concurrency=8
  if ($LASTEXITCODE -ne 0) {
    throw "Remotion render failed for $name with exit code $LASTEXITCODE"
  }
  & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "verify-trial.ps1") -ArtifactPath $artifact -ReceiptPath $receipt
  if ($LASTEXITCODE -ne 0) {
    throw "Artifact verification failed for $name with exit code $LASTEXITCODE"
  }
}

Write-Output "PASS: rendered and verified five local Drive Out drops"
