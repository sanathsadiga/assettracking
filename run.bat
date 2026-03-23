@echo off
REM Asset Tracking System Startup Script for Windows

echo ================================
echo Asset Tracking System - Startup
echo ================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt -q
echo Dependencies installed
echo.

REM Check if .env exists
if not exist ".env" (
    echo .env file not found!
    echo Creating .env from template...
    copy .env.example .env
    echo Created .env file
    echo IMPORTANT: Edit .env with your database credentials
    echo.
)

REM Run migrations
echo Running database migrations...
python manage.py migrate --no-input
echo Migrations completed
echo.

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput --clear -q
echo Static files collected
echo.

REM Start server
echo Starting development server...
echo.
echo ========================================
echo Asset Tracking System is running!
echo ========================================
echo.
echo Access at: http://localhost:8000
echo Admin:    http://localhost:8000/admin/
echo Login:    http://localhost:8000/login/
echo.
echo Press Ctrl+C to stop
echo.

python manage.py runserver
