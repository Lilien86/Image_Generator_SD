#!/bin/bash

# Ensure the script runs from the project directory
cd "$(dirname "$0")"

echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete! Run the app using:"
echo "source venv/bin/activate && python app.py"
