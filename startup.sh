#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Starting Streamlit application..."
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
