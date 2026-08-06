@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if not errorlevel 1 (
  py -m venv .venv
) else (
  python -m venv .venv
)
if errorlevel 1 goto :failed

if not exist ".venv\Scripts\python.exe" (
  echo Failed to create virtual environment.
  goto :failed
)

".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :failed
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :failed
".venv\Scripts\python.exe" -m playwright install chromium
if errorlevel 1 goto :failed
".venv\Scripts\python.exe" -m pytest -q
if errorlevel 1 goto :failed

echo.
echo Setup complete. Run run_windows.bat to start.
pause
exit /b 0

:failed
echo.
echo Setup failed.
pause
exit /b 1
