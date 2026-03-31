@echo off
:: Run the Gmail Notification Service every 3 hours
:: Usage: Right-click and "Run as Administrator"

REM Get the absolute path to the project directory
set PROJECT_DIR=D:\Code\gmail-notification

REM Get Python executable path
for /f "tokens=*" %%i in ('python -c "import sys; print(sys.executable)"') do set PYTHON_EXE=%%i

echo.
echo ============================================================
echo Gmail Notification Service - 3 Hour Scheduler Setup
echo ============================================================
echo.
echo Project Directory: %PROJECT_DIR%
echo Python Executable: %PYTHON_EXE%
echo.

REM Create the scheduled task
schtasks /Create ^
        /SC HOURLY ^
        /MO 3 ^
        /TN "GmailNotification3Hour" ^
        /TR "cmd /c cd /d %PROJECT_DIR% && %PYTHON_EXE% main.py" ^
        /ST 00:00 ^
        /F

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo SUCCESS: Task created/updated!
    echo ============================================================
    echo.
    echo Task Details:
    echo   - Name: GmailNotification3Hour
    echo   - Frequency: Every 3 hours
    echo   - Start Time: 00:00 (midnight)
    echo   - Working Directory: %PROJECT_DIR%
    echo.
    echo The task will run at:
    echo   00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00 daily
    echo.
    echo To view scheduled tasks:
    echo   - Open Task Scheduler (taskschd.msc)
    echo   - Navigate to Task Scheduler Library
    echo   - Look for "GmailNotification3Hour"
    echo.
) else (
    echo.
    echo ERROR: Failed to create task!
    echo Make sure to run this script as Administrator.
    echo.
)

pause
