.PHONY: start dev migrations migrate stop status venv activate

default: dev

dev:activate
	python manage.py runserver

migrations:
	python manage.py makemigrations

migrate:migrations
	python manage.py migrate

start:
	bash scripts/start.sh

stop:
	bash scripts/stop.sh

status:
	bash scripts/status.sh

venv:
	uv sync

activate:venv
	. .venv/bin/activate