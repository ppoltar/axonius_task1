#!/bin/bash

echo "🔧 Setting up your test project..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install project requirements
pip install -r requirements.txt

echo "✅ Setup complete. To activate the virtual environment, run:"
echo "source venv/bin/activate"
