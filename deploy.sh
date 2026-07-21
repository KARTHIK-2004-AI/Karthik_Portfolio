#!/bin/bash
# ==============================================================================
# PythonAnywhere Deployment Script for Karthik Portfolio
# ==============================================================================

set -e  # Exit immediately if a command exits with a non-zero status

echo "=== 1. Pulling latest code ==="
git pull origin main

echo "=== 2. Setting up Virtual Environment ==="
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Created virtual environment 'venv'"
fi

source venv/bin/activate

echo "=== 3. Installing Dependencies ==="
pip install -r requirements.txt

echo "=== 4. Running Database Migrations ==="
python manage.py migrate

echo "=== 5. Collecting Static Files ==="
python manage.py collectstatic --noinput

echo "=== 6. Deployment Complete! ==="
echo "Remember to click 'Reload' in your PythonAnywhere Web Tab."
