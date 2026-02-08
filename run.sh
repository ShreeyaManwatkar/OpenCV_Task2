#!/bin/bash

echo "============================================================"
echo "Member 2 - Gaze Tracking System"
echo "============================================================"
echo ""

if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run ./setup.sh first"
    echo ""
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting gaze tracking system..."
echo ""
cd code
python member2_gaze_tracking.py

cd ..
echo ""
echo "Program ended."
