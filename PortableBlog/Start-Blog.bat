@echo off
setlocal
cd /d "%~dp0"
if not exist "runtime\python.exe" (
  echo Runtime missing. Please extract the entire ZIP before starting.
  pause
  exit /b 1
)
"%~dp0runtime\python.exe" -I "%~dp0blog.py"
if errorlevel 1 (
  echo Blog could not start. See the error above.
  pause
)
endlocal
