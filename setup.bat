@echo off
REM Quick Setup Script for Agricultural Platform Upgrade (Windows)
REM This script sets up the development environment with new requirements

echo 🚀 Agricultural Platform - Phase 1 Setup Script
echo ==============================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install development requirements
echo 📦 Installing development requirements...
pip install -r requirements-dev.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo ⚙️ Creating .env file...
    copy .env.example .env
    echo ⚠️  Please update .env file with your configuration
)

REM Create necessary directories
echo 📁 Creating required directories...
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups
if not exist "media\uploads" mkdir media\uploads

REM Run Django checks
echo 🔍 Running Django system checks...
python manage.py check

REM Check if database migration is needed
echo 🔍 Checking database status...
if exist "db.sqlite3" (
    echo 📊 SQLite database found - migration recommended
    echo 📝 Run: python scripts\migrate_to_postgresql.py
) else (
    echo ✅ No SQLite database found
)

echo.
echo ✅ Setup completed successfully!
echo.
echo Next steps:
echo 1. Update .env file with your configuration
echo 2. Run database migration: python scripts\migrate_to_postgresql.py
echo 3. Start development server: python manage.py runserver
echo.
pause
