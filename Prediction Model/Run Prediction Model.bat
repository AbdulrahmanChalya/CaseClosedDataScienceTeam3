@echo off
setlocal
cd /d "%~dp0"
"%~dp0runtime\python.exe" "%~dp0src\test_churn.py"
if errorlevel 1 pause
