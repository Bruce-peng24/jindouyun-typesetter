@echo off
cd /d "C:\Practice-code\Pandoc-GUI"

echo =====================================
echo Pandoc-GUI Build Tool (with dependency optimization)
echo =====================================
echo.

choice /C YN /M "Enable PyQt5 components and stdlib auto-detection (recommended)?"
if %ERRORLEVEL% == 1 (
    echo [1/3] Detecting PyQt5 components and Python stdlib usage...
    python auto_detect_deps.py
    if %ERRORLEVEL% neq 0 (
        echo Error: Detection failed, continuing with existing configuration...
    )
    echo [2/3] Building application...
) else (
    echo [1/2] Skipping dependency detection, building with existing configuration...
)

REM Build command using spec file
pyinstaller Pandoc-GUI.spec
if %ERRORLEVEL% neq 0 (
    echo Error: Build failed!
    pause
    exit /b 1
)

if %ERRORLEVEL% == 1 (
    echo [3/3] Build complete!
) else (
    echo [2/2] Build complete!
)

echo.
echo Generated exe file located at: dist\Pandoc-GUI.exe
echo.
echo =====================================
echo Note: If the program has issues, check BUILD_GUIDE.md
echo =====================================
pause