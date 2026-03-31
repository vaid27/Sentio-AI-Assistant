@echo off
REM Backend startup script for Windows

echo.
echo =========================================
echo SENTIO AI - BACKEND STARTUP
echo =========================================
echo.

REM Activate virtual environment
echo Activating virtual environment...
call ".venv\Scripts\activate.bat"

REM Initialize database
echo.
echo Initializing database...
python -m backend.init_db

REM Start FastAPI server
echo.
echo Starting FastAPI server...
echo.
echo Server will run at: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.

python -m backend.main
