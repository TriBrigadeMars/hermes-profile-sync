@echo off
REM hermes-sync.bat — Windows wrapper for hermes-sync.sh
REM Use this for Windows Task Scheduler

cd /d "%LOCALAPPDATA%\hermes\sync"
"C:\Program Files\Git\bin\bash.exe" hermes-sync.sh
