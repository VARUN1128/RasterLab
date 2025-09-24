#!/bin/bash

echo "========================================"
echo "    RasterLab Setup Script (Unix)"
echo "========================================"
echo

echo "[1/4] Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/downloads/"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "✓ Python and Node.js found"
echo

echo "[2/4] Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Python dependencies"
    exit 1
fi
echo "✓ Python dependencies installed"
echo

echo "[3/4] Installing Node.js dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Node.js dependencies"
    exit 1
fi
echo "✓ Node.js dependencies installed"
echo

echo "[4/4] Running tests..."
echo "Running backend tests..."
python3 -m pytest tests/test_api.py -v
if [ $? -ne 0 ]; then
    echo "WARNING: Some backend tests failed"
fi

echo "Running frontend tests..."
npm test -- --watchAll=false --passWithNoTests
if [ $? -ne 0 ]; then
    echo "WARNING: Some frontend tests failed"
fi

echo
echo "========================================"
echo "    Setup Complete!"
echo "========================================"
echo
echo "To start the application:"
echo "  1. Terminal 1: python3 backend/main.py"
echo "  2. Terminal 2: npm start"
echo "  3. Browser: http://localhost:3000"
echo
echo "Or run: ./start_application.sh"
echo
