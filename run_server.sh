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
python manage.py load_licenses
python manage.py load_life_cycles

python manage.py collectstatic --noinput

python manage.py makemigrations

python manage.py migrate

# gunicorn --bind 0.0.0.0:8000 --workers 3 config.wsgi:application --reload
gunicorn --bind 0.0.0.0:8000 --workers 3 config.wsgi:application
