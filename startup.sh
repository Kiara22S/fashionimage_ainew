#!/bin/bash

# Force exit on error
set -e

echo "=========================================="
echo "Starting Fashion Image GenAI Application"
echo "=========================================="

# Log environment info
echo "Current working directory: $(pwd)"
echo "Python executable: $(which python)"
echo "Python version: $(python --version 2>&1)"
echo "Pip version: $(python -m pip --version 2>&1)"

# Ensure pip is up to date
echo ""
echo "Step 1: Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel --quiet

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "Step 2: Installing requirements from requirements.txt..."
    python -m pip install -r requirements.txt --quiet
    echo "Requirements installed successfully!"
else
    echo "ERROR: requirements.txt not found in $(pwd)"
    ls -la
    exit 1
fi

# Verify streamlit is installed
echo ""
echo "Step 3: Verifying installations..."
python -m pip list | grep -i streamlit
python -c "import streamlit; print(f'Streamlit version: {streamlit.__version__}')"

# Set default port
PORT=${PORT:-8000}
echo ""
echo "=========================================="
echo "Starting Streamlit on port $PORT"
echo "=========================================="

# Run streamlit
python -m streamlit run app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --logger.level=info \
    --client.showErrorDetails=true
