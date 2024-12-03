sudo apt install redis-server
sudo systemctl restart redis-server
sudo systemctl reload-daemon redis-server
celery -A config worker --beat -l INFO
