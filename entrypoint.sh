#!/bin/bash
set -e

export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

cd /home/site/wwwroot

echo "Installing dependencies..."
python -m pip install --no-cache-dir -r requirements.txt

echo "Starting application..."
python -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0
