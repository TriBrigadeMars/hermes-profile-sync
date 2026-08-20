@echo off
REM ============================================================
REM  Hermes Profile Sync — One-Time Setup Script
REM  Run this on each additional machine (as Administrator)
REM ============================================================

echo.
echo === Hermes Profile Sync Setup ===
echo.

REM Step 1: Check prerequisites
echo [1/5] Checking prerequisites...
where gh >nul 2>&1 || (
    echo ERROR: GitHub CLI not found. Install it from https://cli.github.com/
    pause
    exit /b 1
)
where git >nul 2>&1 || (
    echo ERROR: Git not found. Install it from https://git-scm.com/
    pause
    exit /b 1
)
where hermes >nul 2>&1 || (
    echo ERROR: Hermes not found. Install it first.
    pause
    exit /b 1
)
echo   All prerequisites found.
echo.

REM Step 2: GitHub auth
echo [2/5] Checking GitHub authentication...
gh auth status >nul 2>&1
if errorlevel 1 (
    echo   Not logged in. Opening browser for GitHub login...
    echo   Log in as: TriBrigadeMars
    gh auth login --hostname github.com --web
) else (
    echo   Already logged in as:
    gh auth status 2>&1 | findstr "account"
)
echo.

REM Step 3: Clone sync repo
echo [3/5] Cloning sync repo...
if exist "%LOCALAPPDATA%\hermes\sync" (
    echo   Sync directory already exists, pulling latest...
    cd /d "%LOCALAPPDATA%\hermes\sync"
    git pull origin main
) else (
    cd /d "%LOCALAPPDATA%\hermes"
    git clone https://github.com/TriBrigadeMars/hermes-profile-sync.git sync
)
echo.

REM Step 4: Set permissions
echo [4/5] Setting up scripts...
cd /d "%LOCALAPPDATA%\hermes\sync"
icacls hermes-sync.sh /grant:r "%USERNAME%:R" >nul 2>&1
echo   Done.
echo.

REM Step 5: Create scheduled task
echo [5/5] Creating scheduled task (daily at 4:00 AM MST)...
schtasks /Create /TN "Hermes Profile Sync" /TR "\"C:\Program Files\Git\bin\bash.exe\" \"%LOCALAPPDATA%\hermes\sync\hermes-sync.sh\"" /SC DAILY /ST 04:00 /F
echo.

echo === Setup Complete! ===
echo.
echo   Sync repo:  https://github.com/TriBrigadeMars/hermes-profile-sync
echo   Sync dir:   %LOCALAPPDATA%\hermes\sync
echo   Schedule:   Daily at 4:00 AM MST
echo.
echo   To sync now:  bash "%LOCALAPPDATA%\hermes\sync\hermes-sync.sh"
echo.
pause
