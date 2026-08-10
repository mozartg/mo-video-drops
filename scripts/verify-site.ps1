$ErrorActionPreference = "Stop"
$html = Get-Content -Raw (Join-Path $PSScriptRoot "..\index.html")
$required = @(
  "Drive Out",
  "PAY-FLOOR FIGURE PENDING SOURCED INPUT",
  "assets/driveout-pay-floor-01.mp4",
  "assets/driveout-mileage-log-01.mp4",
  "assets/driveout-pay-floor-longer.mp4",
  "capture-status"
)

foreach ($needle in $required) {
  if ($html.IndexOf($needle, [System.StringComparison]::OrdinalIgnoreCase) -lt 0) {
    throw "Static site is missing required marker: $needle"
  }
}

Write-Output "PASS: static Drive Out surface contains all required markers"
