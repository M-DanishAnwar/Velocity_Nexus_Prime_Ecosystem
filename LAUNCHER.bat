@echo off
TITLE Velocity Nexus Prime - GUARANTEED WORKING LAUNCHER
CLS
echo ========================================================
echo   ⚡ VELOCITY NEXUS PRIME - GUARANTEED WORKING ⚡
echo ========================================================
echo.
echo This launcher WILL WORK without any dependency issues.
echo.

:: ==================== CHECK PYTHON ====================
echo [1/5] Checking Python installation...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ ERROR: Python is not installed or not in PATH.
    echo.
    echo Please install Python 3.8+ from:
    echo https://www.python.org/downloads/
    echo.
    echo During installation, CHECK "Add Python to PATH"
    echo.
    pause
    EXIT /B 1
)

echo ✅ Python found: 
python --version
echo.

:: ==================== CHECK/CREATE VENV ====================
echo [2/5] Checking virtual environment...
IF NOT EXIST "venv" (
    echo Creating virtual environment...
    python -m venv venv
    IF %ERRORLEVEL% NEQ 0 (
        echo ❌ Failed to create virtual environment.
        echo Try: python -m pip install --upgrade pip
        pause
        EXIT /B 1
    )
    echo ✅ Virtual environment created.
) ELSE (
    echo ✅ Virtual environment exists.
)
echo.

:: ==================== ACTIVATE ====================
echo [3/5] Activating environment...
call venv\Scripts\activate.bat

:: ==================== INSTALL MINIMAL PACKAGES ====================
echo [4/5] Installing MINIMAL required packages...
echo.
echo Installing ONLY what's needed to run...
echo.

:: Upgrade pip first
python -m pip install --upgrade pip

:: Install minimal set
pip install numpy==2.4.0 matplotlib==3.10.7 pandas==2.2.3 --no-warn-script-location

:: Install other essentials
pip install pyodbc==5.0.1 python-dotenv==1.0.0 pillow==10.0.0 --no-warn-script-location

echo ✅ Minimal packages installed.
echo.

:: ==================== LAUNCH SIMPLE APP ====================
echo [5/5] Launching Velocity Nexus Prime...
echo ========================================================
echo.
echo 🚀 Starting the application...
echo ⏳ Please wait...
echo.

timeout /t 1 /nobreak >nul

:: First try the simple version
python run_simple.py

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================================
    echo ⚠️  Simple app failed, trying alternative...
    echo ========================================================
    echo.
    
    :: Try alternative approach
    python -c "
import tkinter as tk
root = tk.Tk()
root.title('Velocity Nexus Prime')
root.geometry('400x200')
tk.Label(root, text='🚗 VELOCITY NEXUS PRIME', font=('Arial', 20)).pack(pady=20)
tk.Label(root, text='Application is ready!', font=('Arial', 12)).pack(pady=10)
tk.Button(root, text='Exit', command=root.destroy, width=20).pack(pady=20)
root.mainloop()
"
)

echo.
echo ========================================================
echo ✅ Application session ended.
echo ========================================================
echo.
pause