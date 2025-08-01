@echo off
echo Running ESF Data Visualization Script...
echo.

REM Try different Python executables
echo Trying virtual environment Python...
if exist ".venv\Scripts\python.exe" (
    echo Found .venv Python
    ".venv\Scripts\python.exe" -c "import sys; print('Python executable:', sys.executable)"
    if errorlevel 1 (
        echo .venv Python failed
    ) else (
        echo Installing packages...
        ".venv\Scripts\python.exe" -m pip install pandas numpy matplotlib seaborn
        echo Running visualization script...
        ".venv\Scripts\python.exe" data_visualization_script.py
        goto :end
    )
)

echo Trying conda Python...
if exist ".conda\python.exe" (
    echo Found conda Python
    ".conda\python.exe" data_visualization_script.py
    goto :end
)

echo Trying system Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo No Python found! Please install Python.
) else (
    echo Installing packages...
    python -m pip install pandas numpy matplotlib seaborn
    echo Running visualization script...
    python data_visualization_script.py
)

:end
echo.
echo Script execution completed.
pause
