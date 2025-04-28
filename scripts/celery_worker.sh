#! /bin/bash

source env.sh

celery -A config worker -l INFO
