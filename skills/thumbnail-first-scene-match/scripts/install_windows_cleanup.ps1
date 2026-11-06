# Install an OS-managed cleanup job for thumbnails. Runs every five minutes
# and deletes ONLY expired files in the script's own private preview vault.
$ErrorActionPreference = 'Stop'
$Script = Join-Path $PSScriptRoot 'preview_vault.py'
if (!(Test-Path $Script)) { throw "Missing cleanup script: $Script" }
# pythonw.exe runs without a console window, so the 5-minute job never flashes a window.
$Python = (Get-Command pythonw.exe -ErrorAction SilentlyContinue)
if (!$Python) { $Python = (Get-Command python.exe -ErrorAction SilentlyContinue) }
if (!$Python) { throw 'python.exe not found in PATH. Install Python 3.9+ and retry.' }
$PyExe = $Python.Source
$TaskName = 'ThumbnailFirstSceneMatch-PreviewTTL5h'
$Action = New-ScheduledTaskAction -Execute $PyExe -Argument ('"' + $Script + '" cleanup')
$Trigger = New-ScheduledTaskTrigger -Once -At ((Get-Date).AddMinutes(1)) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 3650)
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 2) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description 'Delete local managed thumbnail preview copies 5 hours after registration' -Force | Out-Null
Write-Output "Registered Task Scheduler job: $TaskName"
Write-Output "Python executable: $PyExe"
Write-Output 'The job requires this computer to run. Files may remain until its next successful execution.'
