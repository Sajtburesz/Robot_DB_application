#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python3 manage.py migrate

# Create superuser
python3 manage.py create_superuser $ADMIN_USERNAME $ADMIN_PASSWORD
# Collect static files
echo "Collect static files"
python3 manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
