@echo off
setlocal DisableDelayedExpansion
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo Virtual environment not found. Please run setup_windows.bat first.
  pause
  exit /b 1
)

set "TARGET_URL="
set /p "TARGET_URL=Enter the page URL to monitor: "
if not defined TARGET_URL (
  echo A target URL is required.
  pause
  exit /b 1
)

".venv\Scripts\python.exe" popup_clicker.py --url "%TARGET_URL%"
set "RUN_EXIT=%errorlevel%"
pause
exit /b %RUN_EXIT%
