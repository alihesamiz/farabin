#! /bin/bash

source env.sh

celery -A config flower --port=5555 --broker=redis://redis:6379/0
