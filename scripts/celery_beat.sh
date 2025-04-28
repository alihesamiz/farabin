#! /bin/bash

source env.sh

celery -A config beat -l INFO
