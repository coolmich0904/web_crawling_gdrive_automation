@echo off
REM Change current directory to batch file location
cd /d "%~dp0"

echo.
echo ======================================================
echo Starting Web Crawling
echo ======================================================
echo.
python webcrawling.py

echo.
echo ======================================================
echo Starting Google Drive Upload
echo ======================================================
echo.
python upload_to_gdrive.py

echo.
echo ======================================================
echo Completed!
echo ======================================================
echo.
pause