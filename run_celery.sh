#!/bin/bash
# apt install redis-server
# systemctl restart redis-server
# systemctl reload-daemon redis-server
celery -A config worker -l INFO
celery -A config beat -l INFO
