#! /bin/bash

source env.sh

celery -A config worker --beat -l INFO
