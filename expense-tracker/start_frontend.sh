#!/bin/bash

echo "Starting Expense Tracker Frontend..."
echo "====================================="

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Start the React development server
echo "Starting React development server..."
echo "The app will open at http://localhost:3000"
echo "Press Ctrl+C to stop the server"
npm start
