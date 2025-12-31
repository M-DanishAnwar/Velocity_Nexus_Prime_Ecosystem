
---

## 📁 **FILE 8: database/backup_database.bat**

```batch
@echo off
TITLE Velocity Nexus Prime - Database Backup Utility
CLS
echo ========================================================
echo   🗄️ VELOCITY NEXUS PRIME DATABASE BACKUP UTILITY 🗄️
echo ========================================================
echo.
echo This utility will backup your database to a specified location.
echo.

:: ==================== CONFIGURATION ====================
set "BACKUP_DIR=H:\Database Backups\VelocityNexusPrime"
set "DB_SERVER=HassanAnwar\SQLEXPRESS"
set "DB_NAME=VelocityNexusPrime"
set "RETENTION_DAYS=30"

:: ==================== CREATE BACKUP DIRECTORY ====================
if not exist "%BACKUP_DIR%" (
    echo Creating backup directory...
    mkdir "%BACKUP_DIR%"
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ Failed to create backup directory.
        echo Please check your path permissions.
        pause
        exit /b 1
    )
)

:: ==================== GENERATE BACKUP FILENAME ====================
set "TIMESTAMP=%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"
set "BACKUP_FILE=%BACKUP_DIR%\VelocityNexusPrime_%TIMESTAMP%.bak"
set "LOG_FILE=%BACKUP_DIR%\backup_log_%TIMESTAMP%.txt"

:: ==================== SHOW CONFIGURATION ====================
echo 📋 BACKUP CONFIGURATION:
echo    Server: %DB_SERVER%
echo    Database: %DB_NAME%
echo    Backup File: %BACKUP_FILE%
echo    Log File: %LOG_FILE%
echo    Retention: %RETENTION_DAYS% days
echo.

:: ==================== CONFIRM BACKUP ====================
set /p CONFIRM="Do you want to proceed with backup? (Y/N): "
if /i "%CONFIRM%" NEQ "Y" (
    echo Backup cancelled.
    pause
    exit /b 0
)

echo.
echo ========================================================
echo 🚀 STARTING DATABASE BACKUP...
echo ========================================================
echo.

:: ==================== PERFORM BACKUP ====================
echo [1/3] Performing full database backup...
echo Backup started at: %DATE% %TIME% > "%LOG_FILE%"

sqlcmd -S %DB_SERVER% -E -Q "
USE master;
GO

BACKUP DATABASE [%DB_NAME%]
TO DISK = '%BACKUP_FILE%'
WITH 
    FORMAT,
    INIT,
    NAME = 'Velocity Nexus Prime Full Backup',
    SKIP,
    STATS = 10,
    COMPRESSION;
GO
" >> "%LOG_FILE%" 2>&1

if %ERRORLEVEL% EQU 0 (
    echo ✅ Database backup completed successfully!
    
    echo [2/3] Verifying backup file...
    sqlcmd -S %DB_SERVER% -E -Q "
    RESTORE VERIFYONLY
    FROM DISK = '%BACKUP_FILE%'
    WITH FILE = 1, NOUNLOAD;
    GO
    " >> "%LOG_FILE%" 2>&1
    
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Backup verification successful!
    ) else (
        echo ⚠️ Backup verification warning (file may still be usable)
    )
) else (
    echo ❌ Database backup failed!
    echo Please check the log file: %LOG_FILE%
    goto :cleanup
)

:: ==================== CLEANUP OLD BACKUPS ====================
echo [3/3] Cleaning up old backups (older than %RETENTION_DAYS% days)...

forfiles /p "%BACKUP_DIR%" /m "*.bak" /d -%RETENTION_DAYS% /c "cmd /c echo Deleting @file..." >> "%LOG_FILE%" 2>&1
forfiles /p "%BACKUP_DIR%" /m "*.bak" /d -%RETENTION_DAYS% /c "cmd /c del /q @path" >> "%LOG_FILE%" 2>&1

forfiles /p "%BACKUP_DIR%" /m "*.txt" /d -%RETENTION_DAYS% /c "cmd /c echo Deleting @file..." >> "%LOG_FILE%" 2>&1
forfiles /p "%BACKUP_DIR%" /m "*.txt" /d -%RETENTION_DAYS% /c "cmd /c del /q @path" >> "%LOG_FILE%" 2>&1

echo ✅ Old backups cleaned up!

:: ==================== GENERATE BACKUP REPORT ====================
echo.
echo ========================================================
echo 📊 BACKUP COMPLETION REPORT
echo ========================================================
echo.

:: Get backup file size
for %%F in ("%BACKUP_FILE%") do (
    set "size=%%~zF"
    set /a sizeMB=!size! / 1048576
)
echo Backup File Size: !sizeMB! MB

:: List all backup files
echo.
echo 📁 AVAILABLE BACKUP FILES:
echo.
dir "%BACKUP_DIR%\*.bak" /B /O:-D

:: Show backup directory info
echo.
echo 📍 BACKUP DIRECTORY INFORMATION:
echo Location: %BACKUP_DIR%
echo Total Space: 
dir "%BACKUP_DIR%"

:: ==================== BACKUP SUMMARY ====================
echo.
echo ========================================================
echo ✅ BACKUP COMPLETED SUCCESSFULLY!
echo ========================================================
echo.
echo 📋 SUMMARY:
echo    - Database: %DB_NAME%
echo    - Server: %DB_SERVER%
echo    - Backup File: %BACKUP_FILE%
echo    - File Size: !sizeMB! MB
echo    - Status: SUCCESS
echo    - Time: %DATE% %TIME%
echo.
echo 🔍 For detailed information, check the log file:
echo    %LOG_FILE%
echo.

:cleanup
:: ==================== OPTIONAL: COPY TO NETWORK ====================
set /p NETWORK_COPY="Do you want to copy backup to network location? (Y/N): "
if /i "%NETWORK_COPY%" EQU "Y" (
    echo Please enter network path (e.g., \\server\backups\):
    set /p NETWORK_PATH="Network Path: "
    
    if not "%NETWORK_PATH%"=="" (
        echo Copying to network location...
        copy "%BACKUP_FILE%" "%NETWORK_PATH%" >> "%LOG_FILE%" 2>&1
        if %ERRORLEVEL% EQU 0 (
            echo ✅ Network copy successful!
        ) else (
            echo ❌ Network copy failed. Please check network connection.
        )
    )
)

:: ==================== OPEN BACKUP DIRECTORY ====================
set /p OPEN_DIR="Open backup directory? (Y/N): "
if /i "%OPEN_DIR%" EQU "Y" (
    explorer "%BACKUP_DIR%"
)

echo.
echo ========================================================
echo 📦 Backup utility completed.
echo ========================================================
echo.
pause