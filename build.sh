#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Create a superuser if one doesn't exist (optional, for initial setup)
# This part is commented out as it's usually done manually or via environment variables
# if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ] && [ "$DJANGO_SUPERUSER_EMAIL" ]; then
#   python manage.py createsuperuser --no-input || true
# fi