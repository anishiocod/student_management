#!/usr/bin/env bash

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (non-interactive)
export DJANGO_SUPERUSER_USERNAME="adminuser"
export DJANGO_SUPERUSER_EMAIL="admin@example.com"
export DJANGO_SUPERUSER_PASSWORD="V3ry$ecur3P@ssw0rd!"

python manage.py createsuperuser --noinput || true

# Collect static files
python manage.py collectstatic --noinput
