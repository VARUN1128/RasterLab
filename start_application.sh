#!/bin/bash

echo "========================================"
echo "    Starting RasterLab Application"
echo "========================================"
echo

echo "Starting backend server..."
python3 backend/main.py &
BACKEND_PID=$!

echo "Waiting for backend to start..."
sleep 3

echo "Starting frontend server..."
npm start &
FRONTEND_PID=$!

echo
echo "========================================"
echo "    Application Started!"
echo "========================================"
echo
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo
echo "Press Ctrl+C to stop both servers"
echo

# Function to cleanup on exit
cleanup() {
    echo "Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
