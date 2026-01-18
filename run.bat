@echo off
echo ========================================
echo Plagiarism Checker - Desktop Application
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Starting Plagiarism Checker...
echo.

python plagiarism_checker_gui.py

if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)
