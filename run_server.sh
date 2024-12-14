#!/bin/bash

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Load necessary data
python manage.py load_departments
python manage.py load_cities
python manage.py load_special_fields
python manage.py load_tech_fields
python manage.py load_services

# Collect static files
python manage.py collectstatic --noinput

# Make migrations again (just to be sure)
python manage.py makemigrations

# Apply migrations again (in case new migrations were created)
python manage.py migrate

# Start the application using Gunicorn
# You may need to adjust the number of workers (workers=3) depending on your app's needs
# Adjust the app_name (usually it's the name of your Django project, for example, myproject.wsgi:application)
gunicorn --bind 0.0.0.0:8000 --workers 2 config.wsgi:application
# python manage.py runserver 127.0.0.1:8000
