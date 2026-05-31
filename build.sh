#!/usr/bin/env bash
# exit on error
set -o errexit

echo "==> Upgrading pip..."
pip install --upgrade pip

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Compiling static assets..."
python manage.py collectstatic --no-input

echo "==> Executing database migrations..."
python manage.py migrate

echo "==> Executing initial database seeder..."
python seed.py

echo "==> Build successfully completed!"
