#!/bin/bash
# Quick Start Script for 5-Axis DED Slicer
# This script runs all the demonstrations in sequence

echo "=========================================="
echo "5-Axis DED Slicer - Quick Start"
echo "=========================================="
echo ""
echo "This will run all demonstrations in sequence."
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found."
    echo "Please install Python 3 and try again."
    exit 1
fi

echo "Python 3 found: $(python3 --version)"
echo ""

# Run the main demo
echo "=========================================="
echo "1. Running Main Demo..."
echo "=========================================="
python3 demo.py
if [ $? -ne 0 ]; then
    echo "Error running demo.py"
    exit 1
fi

echo ""
echo "=========================================="
echo "2. Running Unit Tests..."
echo "=========================================="
python3 test_slicer.py
if [ $? -ne 0 ]; then
    echo "Warning: Some tests failed"
fi

echo ""
echo "=========================================="
echo "3. Running Visualizations..."
echo "=========================================="
python3 visualize.py
if [ $? -ne 0 ]; then
    echo "Error running visualize.py"
    exit 1
fi

echo ""
echo "=========================================="
echo "4. Generating Example Parts..."
echo "=========================================="
python3 slicer_5axis.py
if [ $? -ne 0 ]; then
    echo "Error running slicer_5axis.py"
    exit 1
fi

echo ""
echo "=========================================="
echo "Quick Start Complete!"
echo "=========================================="
echo ""
echo "Generated G-code files:"
ls -lh *.gcode 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
echo ""
echo "Try these commands for more examples:"
echo "  python3 examples.py     # Detailed examples"
echo "  python3 demo.py         # Quick demo"
echo "  python3 visualize.py    # Visualizations"
echo ""
echo "See SLICER_README.md for complete documentation."
echo ""
