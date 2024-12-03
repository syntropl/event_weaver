#!/bin/bash

# Exit script on error
set -e

# Detect OS
OS=$(uname -s | tr '[:upper:]' '[:lower:]')

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH."
    exit 1
fi

# Create a virtual environment using Python 3
python3 -m venv event_weaver_venv

# Activate the virtual environment
if [[ "$OS" == "mingw"* || "$OS" == "cygwin"* || "$OS" == *"nt"* ]]; then
    # Windows
    source event_weaver_venv/Scripts/activate
else
    # Linux/Mac
    source event_weaver_venv/bin/activate
fi

# Ensure pip is up to date
pip install --upgrade pip

# Install dependencies
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found. Skipping dependency installation."
fi
