@echo off
REM FMCG SaaS Platform - Quick Setup Script for Windows

echo ========================================
echo FMCG SaaS Platform Setup
echo ========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
echo Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo Pip upgraded
echo.

REM Install dependencies
echo Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt
echo Dependencies installed
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo .env file created
    echo.
    echo WARNING: Edit .env file and add your API keys:
    echo    - GROQ_API_KEY (get from https://console.groq.com)
    echo    - DATABASE_URL (optional, get from https://supabase.com)
    echo.
) else (
    echo .env file already exists
    echo.
)

echo ========================================
echo Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file with your API keys
echo 2. Run: streamlit run app.py
echo 3. Open browser at http://localhost:8501
echo.
echo For deployment to Streamlit Cloud, see DEPLOYMENT.md
echo ========================================
pause
