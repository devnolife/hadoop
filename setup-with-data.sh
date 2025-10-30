#!/bin/bash
# Quick Setup with Sample Data
# Author: devnolife

echo "========================================"
echo "  Hadoop Toolkit - Quick Setup"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "[1/4] Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "[2/4] Activating virtual environment..."
source .venv/bin/activate

echo ""
echo "[3/4] Installing dependencies..."
pip install -q -r requirements-web.txt
echo "✓ Dependencies installed"

echo ""
echo "[4/4] Creating sample data..."
echo ""
echo "============================================"
echo "  Sample Data Generator"
echo "============================================"
echo "This will create a test database with:"
echo "  - 100 Products"
echo "  - 50 Customers"
echo "  - 200 Orders"
echo "  - 1 Sales Summary View"
echo "============================================"
echo ""
python3 examples/create_sample_data.py

echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "Next step: Run the web interface"
echo "  Command: python app.py"
echo "  URL: http://localhost:5000"
echo ""
