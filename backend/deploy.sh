#!/bin/bash
set -e

echo "Setting up Python environment..."

# Create virtual environment
python3.11 -m venv --copies /opt/venv
source /opt/venv/bin/activate

# Upgrade pip and install build tools
pip install --upgrade pip setuptools wheel

# Set environment variables to prefer pre-built wheels
export PIP_PREFER_BINARY=1
export PIP_NO_CACHE_DIR=1

# Install packages with specific flags to avoid compilation
pip install --no-cache-dir --only-binary=all -r requirements.txt

echo "Python environment setup complete!"
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"
