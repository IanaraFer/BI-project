@echo off
echo ESF Data Analysis - Running Fixed Version
echo ==========================================

echo.
echo Checking Python environment...
"C:\Users\35387\AppData\Local\anaconda3\Scripts\conda.exe" run -p "c:\Users\35387\Desktop\BI project\.conda" python --version

echo.
echo Running ESF Analysis (Fixed Version)...
"C:\Users\35387\AppData\Local\anaconda3\Scripts\conda.exe" run -p "c:\Users\35387\Desktop\BI project\.conda" python basic_analysis_script_fixed.py

echo.
echo Analysis completed! Press any key to exit...
pause
