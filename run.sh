#!/bin/bash

echo "========================================"
echo "Plagiarism Checker - Desktop Application"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3 first"
    exit 1
fi

echo "Starting Plagiarism Checker..."
echo ""

python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Application exited with an error."
    read -p "Press Enter to continue..."
fi
