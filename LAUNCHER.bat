@echo off
TITLE Velocity Nexus Prime - Environment Manager
CLS
echo ========================================================
echo   VELOCITY NEXUS PRIME - AUTOMATED DEPLOYMENT SYSTEM
echo ========================================================
echo.

:: 1. Check for Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in System PATH.
    echo Please install Python 3.x and check "Add to PATH" in the installer.
    PAUSE
    EXIT
)

:: 2. Check/Create Virtual Environment
IF NOT EXIST "venv" (
    echo [INFO] Virtual Environment not found. Creating 'venv'...
    python -m venv venv
    IF %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to create venv.
        PAUSE
        EXIT
    )
    echo [SUCCESS] venv created.
)

:: 3. Activate Environment & Install Requirements
echo [INFO] Activating Environment and Checking Dependencies...
call venv\Scripts\activate
pip install -r requirements.txt >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Installing dependencies for the first time...
    pip install pyodbc pillow tk
)

:: 4. Run the Application
echo.
echo [INFO] Environment Ready. Launching Application...
echo ========================================================
python run.py

:: 5. Catch Crash
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [CRITICAL ERROR] The application crashed.
    echo Read the error message above.
    PAUSE
)
PAUSE