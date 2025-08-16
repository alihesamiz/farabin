#!/bin/bash

source env.sh

WORKERS=$(python -c "import os; print(os.cpu_count())")
FARABIN_PORT=$(python -c "import os; print(os.getenv('FARABIN_PORT', '8000'))")
python manage.py migrate

# python manage.py load_departments
python manage.py load_cities
python manage.py load_special_fields
python manage.py load_tech_fields
# python manage.py load_services
python manage.py load_excel_files
python manage.py load_licenses
python manage.py load_life_cycles
python manage.py load_swot_questions

python manage.py collectstatic --noinput

gunicorn --bind 0.0.0.0:"$FARABIN_PORT" --workers "$WORKERS" config.wsgi:application
