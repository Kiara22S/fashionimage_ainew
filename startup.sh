#!/bin/bash
set -e

echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

echo "Installing Python dependencies..."
python -m pip install --upgrade pip setuptools wheel

if [ -f "requirements.txt" ]; then
    echo "Found requirements.txt, installing dependencies..."
    python -m pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found"
fi

echo "Dependencies installed successfully"
echo "Starting Streamlit application..."

# Set port default if not specified
PORT=${PORT:-8000}

# Run streamlit with proper configuration
python -m streamlit run app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --logger.level=info
