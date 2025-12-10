@echo off
echo Starting Expense Tracker Frontend...
echo =====================================

cd frontend

REM Check if node_modules exists
if not exist "node_modules\" (
    echo Installing dependencies...
    call npm install
)

REM Start the React development server
echo Starting React development server...
echo The app will open at http://localhost:3000
echo Press Ctrl+C to stop the server
call npm start

pause
