#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Load sample data
echo "Loading sample data..."
python setup.py

# Start server
echo "Starting server..."
exec gunicorn djCMS.wsgi:application --bind 0.0.0.0:${PORT:-8000}