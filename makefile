.PHONY: start dev migrations migrate stop status

dev:
	python manage.py runserver

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

start:
	bash scripts/start.sh

stop:
	bash scripts/stop.sh

status:
	bash scripts/status.sh