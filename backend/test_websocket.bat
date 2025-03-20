@echo off
echo Testing Virtual Teacher WebSocket Connection...
echo.
echo This script will test the connection to the WebSocket server.
echo Make sure the server is running before executing this test.
echo.
echo Default audio file path: C:\UnrealAudio\input.wav
echo.

set /p audio_path=Enter audio file path (or press Enter for default): 

if "%audio_path%"=="" (
    set audio_path=C:\UnrealAudio\input.wav
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

echo Testing WebSocket connection...
python scripts/test_websocket.py --audio "%audio_path%"

echo.
pause 