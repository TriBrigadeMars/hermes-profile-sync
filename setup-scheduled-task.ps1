# setup-scheduled-task.ps1
# Creates the "Hermes Profile Sync" scheduled task on this machine, including
# the missed-start failsafe (StartWhenAvailable) so a sync skipped because the
# PC was asleep at 4 AM runs as soon as the machine wakes.
#
# Idempotent — safe to run repeatedly. No admin rights needed for a daily
# trigger (the AtLogon trigger would require admin; this uses daily only).
#
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File setup-scheduled-task.ps1
#   powershell -NoProfile -ExecutionPolicy Bypass -File setup-scheduled-task.ps1 -Time "06:30"

param(
    [string]$TaskName = "Hermes Profile Sync",
    [string]$Time = "04:00",
    [int]$ExecutionMinutes = 15
)

$ErrorActionPreference = "Stop"

$syncDir = Join-Path $env:LOCALAPPDATA "hermes\sync"
$scriptPath = Join-Path $syncDir "hermes-sync.sh"
$bash = "C:\Program Files\Git\bin\bash.exe"

if (-not (Test-Path $scriptPath)) {
    Write-Host "ERROR: hermes-sync.sh not found at $scriptPath" -ForegroundColor Red
    Write-Host "Clone the repo first:  git clone https://github.com/TriBrigadeMars/hermes-profile-sync.git `"$syncDir`""
    exit 1
}

$action = New-ScheduledTaskAction -Execute $bash -Argument ('"{0}"' -f $scriptPath) -WorkingDirectory $syncDir
$trigger = New-ScheduledTaskTrigger -Daily -At ([datetime]::Parse($Time))
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes $ExecutionMinutes)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger `
    -Settings $settings -Principal $principal `
    -Description "Daily Hermes profile sync to GitHub (TriBrigadeMars/hermes-profile-sync)" -Force | Out-Null

$t = Get-ScheduledTask -TaskName $TaskName
Write-Host "Scheduled task '$TaskName' is ready." -ForegroundColor Green
Write-Host ("  Daily at {0}, auto catch-up on wake (StartWhenAvailable): {1}" -f $Time, $t.Settings.StartWhenAvailable)
Write-Host "  Run now with:  Start-ScheduledTask -TaskName '$TaskName'"
