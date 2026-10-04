@echo off
setlocal
cd /d "%~dp0"
"%~dp0runtime\python.exe" "%~dp0src\verify_bundle.py"
pause
