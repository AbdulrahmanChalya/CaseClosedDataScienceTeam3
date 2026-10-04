@echo off
setlocal
cd /d "%~dp0"
if not exist "%~dp0data\subscribers.csv" (
    echo Place your training CSV at data\subscribers.csv before retraining.
    pause
    exit /b 1
)
"%~dp0runtime\python.exe" "%~dp0src\train_churn.py" --input "%~dp0data\subscribers.csv" --output "%~dp0reports\churn_model"
pause
