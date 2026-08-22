@echo off
REM hermes-sync.bat — Windows wrapper for hermes-sync.sh
REM Use this for Windows Task Scheduler
REM Syncs profiles, scripts, and cron jobs across machines.

cd /d "%~dp0"
"C:\Program Files\Git\bin\bash.exe" hermes-sync.sh
