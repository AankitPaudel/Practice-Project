@echo off
echo Creating Test Audio File for WebSocket Testing...
echo.
echo This script will create a test audio file for WebSocket testing.
echo Default output path: C:\UnrealAudio\input.wav
echo.

set /p output_path=Enter output path (or press Enter for default): 

if "%output_path%"=="" (
    set output_path=C:\UnrealAudio\input.wav
)

cd %~dp0
echo Current directory: %CD%

REM Activate virtual environment if it exists
if exist "..\venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "..\venv\Scripts\activate.bat"
) else (
    echo Warning: Virtual environment not found at ..\venv
    echo Using system Python installation.
)

echo Creating test audio file...
python scripts/create_test_audio.py --output "%output_path%"

echo.
pause 