@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo  Fix Gridea absolute URLs
echo ============================================
echo.
python fix-urls.py
echo.
pause
