#!/bin/bash

echo "============================================================"
echo "Member 2 - Gaze Tracking System Setup"
echo "============================================================"
echo ""

echo "Step 1: Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    echo "Make sure Python 3 is installed"
    exit 1
fi
echo "✓ Virtual environment created"
echo ""

echo "Step 2: Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi
echo "✓ Virtual environment activated"
echo ""

echo "Step 3: Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"
echo ""

echo "============================================================"
echo "Setup Complete! ✓"
echo "============================================================"
echo ""
echo "To run the program:"
echo "  1. Run: ./run.sh"
echo "  OR"
echo "  2. Activate venv: source venv/bin/activate"
echo "     Then run: cd code && python member2_gaze_tracking.py"
echo ""
