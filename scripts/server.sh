#!/bin/bash

source env.sh

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
python manage.py load_swot_questions

python manage.py collectstatic --noinput

python manage.py makemigrations
python manage.py migrate

gunicorn --bind 0.0.0.0:8000 --workers 3 config.wsgi:application
# gunicorn --bind 0.0.0.0:8000 --workers 3 config.wsgi:application
