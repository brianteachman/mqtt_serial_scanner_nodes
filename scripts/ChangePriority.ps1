# Setup Instructions
# -----------------------------------------------------------------------------
# 1.) Allow scripts to be run on system. From elevated Powershell, run:
#     PS> Set-ExecutionPolicy unrestricted
# 
# 2.) Verify new policy:
#     PS> Get-ExecutionPolicy
# 
# 3.) Setup a scheduled task to run every 5 minutes that runs this script.
#     PS> schtasks /Create /tn "Process Priority Change" /sc MINUTE /mo 5 /ru SYSTEM /tr "powershell -noprofile -executionpolicy bypass -file \"%cd%\ChangePriority.ps1\""

Get-WmiObject Win32_process -Filter 'name="pythonservice.exe"' | ForEach-Object {$_.SetPriority(128)}

# References: 
#   https://serverfault.com/a/962996
#   https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/setpriority-method-in-class-win32-process