@Echo Off

setlocal
cd /d %~dp0

C:\Users\sgtamdp\AppData\Local\GfK\EvoRep\App\EvoRep.exe

TIMEOUT 3

python "C:\SGTAM_DP\Working Project\BackupDNXZip\BackUpLatestDNXZip.py"

