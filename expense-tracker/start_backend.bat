@echo off
echo Starting Expense Tracker Backend...
echo ==================================

cd backend

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install/Update dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Start the Flask server
echo Starting Flask server on http://localhost:5000
echo Press Ctrl+C to stop the server
python app.py

pause
