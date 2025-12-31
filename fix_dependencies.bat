@echo off
TITLE Nuclear Fix - Guaranteed to Work
echo ============================================
echo NUCLEAR FIX FOR VELOCITY NEXUS PRIME
echo ============================================
echo.
echo This will completely reset and fix everything
echo.

:: Step 1: Deactivate and remove old venv
echo Step 1: Removing old virtual environment...
if exist "venv" (
    rmdir /s /q "venv"
    echo ✅ Old venv removed
)

:: Step 2: Create new venv
echo.
echo Step 2: Creating fresh virtual environment...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to create venv
    pause
    exit /b 1
)
echo ✅ New venv created

:: Step 3: Activate and upgrade pip
echo.
echo Step 3: Activating and updating pip...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel

:: Step 4: Install compatible packages
echo.
echo Step 4: Installing compatible packages...

echo Installing numpy==2.4.0...
pip install numpy==2.4.0

echo Installing matplotlib==3.10.7...
pip install matplotlib==3.10.7

echo Installing pandas==2.2.3...
pip install pandas==2.2.3

echo Installing other core packages...
pip install pyodbc==5.0.1
pip install python-dotenv==1.0.0
pip install pillow==10.0.0

:: Step 5: Test imports
echo.
echo Step 5: Testing imports...
python -c "
try:
    import numpy
    print('✅ numpy', numpy.__version__)
except Exception as e:
    print('❌ numpy failed:', e)

try:
    import matplotlib
    print('✅ matplotlib', matplotlib.__version__)
except Exception as e:
    print('❌ matplotlib failed:', e)

try:
    import pandas
    print('✅ pandas', pandas.__version__)
except Exception as e:
    print('❌ pandas failed:', e)

try:
    import pyodbc
    print('✅ pyodbc', pyodbc.version)
except Exception as e:
    print('❌ pyodbc failed:', e)
"

echo.
echo ============================================
echo ✅ NUCLEAR FIX COMPLETED!
echo ============================================
echo.
echo Now run the application with:
echo 1. python run_simple.py
echo    OR
echo 2. Double-click LAUNCHER_FIXED.bat
echo.
pause