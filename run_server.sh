#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/.env" ]; then
    echo "Loading environment variables from .env file in $SCRIPT_DIR..."
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
    echo "Done Loading..."
else
    echo "No .env file found in $SCRIPT_DIR."
    exit 1
fi


python manage.py makemigrations --noinput

python manage.py migrate --noinput

python manage.py load_departments
python manage.py load_cities
python manage.py load_special_fields
python manage.py load_tech_fields
python manage.py load_services 
python manage.py load_excel_files 

python manage.py collectstatic --noinput

python manage.py makemigrations

python manage.py migrate

# Start the application using Gunicorn
# You may need to adjust the number of workers (workers=3) depending on your app's needs
# Adjust the app_name (usually it's the name of your Django project, for example, myproject.wsgi:application)
gunicorn --bind 0.0.0.0:8000 --workers 2 config.wsgi:application
# gunicorn --workers=3 --worker-class=sync --timeout=30 config.wsgi:application
# gunicorn --log-level=debug config.wsgi:application

# python manage.py runserver
