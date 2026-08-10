[CmdletBinding()]
param(
    [string]$TaskName = 'MoMediaRevenueReleaseFactory',
    [string]$WeeklyDay = 'Sunday',
    [string]$At = '06:10'
)

$ErrorActionPreference = 'Stop'
$runner = Join-Path $PSScriptRoot 'run-media-release.ps1'
$time = [datetime]::ParseExact($At, 'HH:mm', $null)
$action = New-ScheduledTaskAction `
    -Execute 'powershell.exe' `
    -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$runner`""
$trigger = New-ScheduledTaskTrigger -Weekly -WeeksInterval 1 -DaysOfWeek $WeeklyDay -At $time
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2) `
    -MultipleInstances IgnoreNew
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description 'Builds a receipt-backed nine-day cross-brand ready-to-post media queue in synced Google Drive.' `
    -Force | Out-Null

$task = Get-ScheduledTask -TaskName $TaskName
$info = Get-ScheduledTaskInfo -TaskName $TaskName
[pscustomobject]@{
    TaskName = $task.TaskName
    State = $task.State.ToString()
    NextRunTime = $info.NextRunTime
    Runner = $runner
} | ConvertTo-Json

