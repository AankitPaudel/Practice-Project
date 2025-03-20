@echo off
echo Virtual Teacher WebSocket Tools
echo ==============================
echo.
echo This script provides tools for working with WebSockets in the Virtual Teacher project.
echo.
echo 1. Start WebSocket Server
echo 2. Test WebSocket Connection
echo 3. Create Test Audio File
echo 4. Install Dependencies
echo 5. Exit
echo.

:menu
set /p choice=Enter your choice (1-5): 

if "%choice%"=="1" (
    cls
    echo Starting WebSocket Server...
    call start_websocket_server.bat
    goto end
)

if "%choice%"=="2" (
    cls
    echo Testing WebSocket Connection...
    call test_websocket.bat
    goto end
)

if "%choice%"=="3" (
    cls
    echo Creating Test Audio File...
    call create_test_audio.bat
    goto end
)

if "%choice%"=="4" (
    cls
    echo Installing Dependencies...
    cd %~dp0
    
    REM Activate virtual environment if it exists
    if exist "..\venv\Scripts\activate.bat" (
        echo Activating virtual environment...
        call "..\venv\Scripts\activate.bat"
    ) else (
        echo Warning: Virtual environment not found at ..\venv
        echo Using system Python installation.
    )
    
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    
    echo.
    pause
    goto menu
)

if "%choice%"=="5" (
    goto end
)

echo Invalid choice. Please try again.
goto menu

:end
echo.
echo Thank you for using Virtual Teacher WebSocket Tools! 