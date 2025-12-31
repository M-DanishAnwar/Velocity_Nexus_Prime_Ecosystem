@echo off
TITLE Velocity Nexus Prime - Repair Tool
CLS
echo ========================================================
echo   REPAIRING PYTHON ENVIRONMENT
echo   Target: Python 3.12 Compatibility
echo ========================================================
echo.

:: 1. Navigate to project directory
cd /d "%~dp0"

:: 2. Create/Activate Virtual Environment
IF NOT EXIST "venv" (
    echo [1/4] Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat

:: 3. Clean unstable packages
echo [2/4] Uninstalling conflicting packages...
pip uninstall -y numpy pandas matplotlib

:: 4. Install STABLE versions for Python 3.12
echo [3/4] Installing compatible versions...
echo.
echo Installing NumPy 1.26.4 (Critical for Py3.12)...
pip install "numpy==1.26.4"

echo Installing Pandas 2.1.4...
pip install "pandas==2.1.4"

echo Installing Matplotlib 3.8.2...
pip install "matplotlib==3.8.2"

echo Installing remaining dependencies...
pip install pyodbc==5.0.1 python-dotenv==1.0.0 pillow==10.2.0

echo.
echo [4/4] Verifying installation...
python -c "import numpy; import pandas; import matplotlib; print('SUCCESS: All libraries imported correctly!')"

IF %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo   REPAIR COMPLETE - YOU CAN NOW USE LAUNCHER.BAT
    echo ========================================================
) ELSE (
    echo.
    echo   REPAIR FAILED - Please check internet connection.
)
pause