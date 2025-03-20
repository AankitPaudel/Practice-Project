@echo off
echo Starting Virtual Teacher WebSocket Server...
echo.
echo This server enables real-time voice communication between Unreal Engine and AI.
echo.
echo Press Ctrl+C to stop the server.
echo.

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

echo Starting server...
python scripts/run_websocket_server.py

pause 