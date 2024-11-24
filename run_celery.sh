sudo systemctl restart redis-server
celery -A config worker -l INFO
