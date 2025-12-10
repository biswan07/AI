#!/bin/bash

echo "Starting Expense Tracker Backend..."
echo "=================================="

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/Update dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Start the Flask server
echo "Starting Flask server on http://localhost:5000"
echo "Press Ctrl+C to stop the server"
python app.py
