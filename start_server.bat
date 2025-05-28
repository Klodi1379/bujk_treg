@echo off
echo ====================================
echo   Agricultural Platform - Setup
echo ====================================

echo.
echo [1/4] Aktivizimi i virtual environment...
call venv_313\Scripts\activate.bat

echo.
echo [2/4] Kontrollimi i sistemit...
python manage.py check --settings=agricultural_platform.settings_simple

echo.
echo [3/4] Migrations...
python manage.py migrate --settings=agricultural_platform.settings_simple

echo.
echo [4/4] Startimi i serverit...
echo.
echo Serveri po startohet në: http://127.0.0.1:8000
echo Shtypni Ctrl+C për të ndalur serverin
echo.
python manage.py runserver --settings=agricultural_platform.settings_simple

pause
