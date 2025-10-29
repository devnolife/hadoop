#!/bin/bash
# Quick Start Script - Linux/Mac
# Author: devnolife

echo "========================================"
echo "Hadoop Web Interface - Quick Start"
echo "Created by devnolife"
echo "========================================"
echo ""

# Check Python
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python not found! Please install Python 3.8+"
    exit 1
fi
python3 --version
echo ""

# Create virtual environment
echo "[2/5] Setting up virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Virtual environment created!"
else
    echo "Virtual environment already exists!"
fi
echo ""

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source .venv/bin/activate
echo ""

# Install dependencies
echo "[4/5] Installing dependencies..."
pip install -r requirements-web.txt
echo ""

# Start application
echo "[5/5] Starting web application..."
echo ""
echo "========================================"
echo "Web interface will open at:"
echo "http://localhost:5000"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
