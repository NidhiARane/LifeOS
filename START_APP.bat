@echo off
REM LifeOS Application Launcher
REM Runs the LifeOS Flask application with all modules

cd /d "E:\WebBasedProjects\Life OS - BCA Project\LifeOS"

echo.
echo ======================================================================
echo                     LifeOS - Life Management System
echo ======================================================================
echo.
echo Starting Flask Application...
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

REM Activate virtual environment
call .\venv\Scripts\activate.bat

echo.
echo ======================================================================
echo                        Application Information
echo ======================================================================
echo.
echo Web URL:        http://localhost:5000
echo Database:       lifeos_dev.db (SQLite)
echo.
echo MODULES AVAILABLE:
echo   Module 1: User & System Management (Login, Profile, Admin)
echo   Module 2: Smart Finance & Grocery Management (NEW!)
echo       - Finance Dashboard:  http://localhost:5000/finance/dashboard
echo       - Expenses:           http://localhost:5000/finance/expenses
echo       - Budget Analysis:    http://localhost:5000/finance/budget
echo       - AI Insights:        http://localhost:5000/finance/insights
echo       - Grocery Dashboard:  http://localhost:5000/grocery/dashboard
echo       - Shopping List:      http://localhost:5000/grocery/shopping-list
echo.
echo QUICK START:
echo   1. Open http://localhost:5000 in your browser
echo   2. Login/Register an account
echo   3. Go to Dashboard
echo   4. Click "Finance Dashboard" or "Grocery Management"
echo.
echo Press CTRL+C to stop the server
echo.
echo ======================================================================
echo.

REM Run the app
python run.py

pause

