@echo off
echo ========================================
echo LastKings Liquor Store POS System
echo Installation
echo ========================================
echo.
echo Installing required packages...
py -m pip install pyserial pywin32
echo.
echo Adding sample products to database...
py sample_products.py
echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the POS system, run: run.bat
echo Or type: py pos_system.py
echo.
pause