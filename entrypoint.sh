#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
sleep 5

# Check database connection
echo "Checking database connection..."
python check_db.py || {
    echo "Database check failed. Continuing with setup anyway..."
}

# Create migrations if they don't exist
echo "Creating migrations..."
python manage.py makemigrations core
python manage.py makemigrations theming
python manage.py makemigrations pages
python manage.py makemigrations categories
python manage.py makemigrations navigation
python manage.py makemigrations blog
python manage.py makemigrations widgets
python manage.py makemigrations newsletter
python manage.py makemigrations media_library
python manage.py makemigrations comments
python manage.py makemigrations search

# Apply database migrations with retries
echo "Applying database migrations..."
for i in {1..5}; do
    python manage.py migrate && break || {
        echo "Migration attempt $i failed. Retrying in 5 seconds..."
        sleep 5
    }
done

# Check if migrations were successful
python check_db.py || {
    echo "Database setup failed after multiple attempts."
    exit 1
}

# Load sample data
echo "Loading sample data..."
python setup.py

# Start server
echo "Starting server..."
exec gunicorn djCMS.wsgi:application --bind 0.0.0.0:${PORT:-8000}