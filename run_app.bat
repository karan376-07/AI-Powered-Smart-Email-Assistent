@echo off
:: Set console properties
title AI Powered Smart Email Assistant Launcher

:: Check for command-line arguments to bypass menu
if "%~1"=="--start" goto launch
if "%~1"=="/start" goto launch

color 0B
mode con: cols=85 lines=25

:menu
cls
echo =====================================================================================
echo                AI-POWERED SMART EMAIL ASSISTANT LAUNCHER
echo =====================================================================================
echo.
echo    [1] Start Application (Launch Backend, Frontend, and Browser)
echo    [2] Create Desktop Shortcut (Create a convenient double-click link on Desktop)
echo    [3] Exit
echo.
echo =====================================================================================
set /p choice="  Enter your choice (1-3): "

if "%choice%"=="1" goto launch
if "%choice%"=="2" goto shortcut
if "%choice%"=="3" exit
goto menu

:launch
cls
echo =====================================================================================
echo    Launching AI-Powered Smart Email Assistant...
echo =====================================================================================
echo.

:: 1. Start Backend FastAPI Server
echo  [+] Starting Backend Server (FastAPI)...
if not exist "%~dp0backend\venv" (
    color 0C
    echo.
    echo  [!] ERROR: Python virtual environment not found in backend\venv
    echo      Please run setup first or check your backend directory.
    echo.
    pause
    color 0B
    goto menu
)
cd /d "%~dp0backend"
start "Email Assistant Backend" cmd /k "title Email Assistant Backend && echo Starting Backend FastAPI Server... && venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000"

:: 2. Start Frontend Vite Server
echo  [+] Starting Frontend Server (Vite)...
if not exist "%~dp0frontend\node_modules" (
    color 0C
    echo.
    echo  [!] ERROR: node_modules folder not found in frontend\node_modules
    echo      Please run "npm install" inside the frontend directory first.
    echo.
    pause
    color 0B
    goto menu
)
cd /d "%~dp0frontend"
start "Email Assistant Frontend" cmd /k "title Email Assistant Frontend && echo Starting Frontend Vite Server... && npm run dev"

:: Return to root directory
cd /d "%~dp0"

:: 3. Wait and launch browser
echo.
echo  [+] Waiting 3 seconds for servers to initialize...
ping 127.0.0.1 -n 4 > nul

echo  [+] Opening application at http://localhost:5173...
start http://localhost:5173

echo.
echo =====================================================================================
echo    Application successfully started!
echo    - Backend is running on http://localhost:8000
echo    - Frontend is running on http://localhost:5173
echo.
echo    Keep the backend and frontend command windows open while using the app.
echo =====================================================================================
echo.
if "%~1"=="--start" exit
if "%~1"=="/start" exit
pause
goto menu

:shortcut
cls
echo =====================================================================================
echo    Creating Desktop Shortcut...
echo =====================================================================================
echo.

powershell -NoProfile -Command ^
    "$wshell = New-Object -ComObject WScript.Shell; " ^
    "$desktop = [System.Environment]::GetFolderPath('Desktop'); " ^
    "$shortcut = $wshell.CreateShortcut(\"$desktop\AI Powered Smart Email Assistant.lnk\"); " ^
    "$shortcut.TargetPath = '%~f0'; " ^
    "$shortcut.Arguments = '--start'; " ^
    "$shortcut.WorkingDirectory = '%~dp0'; " ^
    "$shortcut.IconLocation = 'shell32.dll,156'; " ^
    "$shortcut.Description = 'Launch AI-Powered Smart Email Assistant'; " ^
    "$shortcut.Save()"

if %errorlevel% equ 0 (
    echo  [+] Desktop shortcut 'AI Powered Smart Email Assistant' created successfully!
    echo      You can now double-click it on your Desktop to open the application anytime.
) else (
    color 0C
    echo  [!] Failed to create Desktop shortcut. Please run this script as Administrator.
    color 0B
)
echo.
pause
goto menu
