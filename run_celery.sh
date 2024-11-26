sudo systemctl restart redis-server
celery -A config worker --beat -l INFO
