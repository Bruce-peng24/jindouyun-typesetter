@echo off
cd /d "C:\Practice-code\Pandoc-GUI"

echo Rebuilding Pandoc-GUI with all necessary dependencies...
echo This script uses the configuration that successfully built your app
echo.

REM Build command using spec file
pyinstaller Pandoc-GUI.spec

echo.
echo Build complete! Executable located at dist\Pandoc-GUI.exe
echo Press any key to exit...
pause > nul