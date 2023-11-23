#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
