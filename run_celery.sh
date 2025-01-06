#!/bin/bash
# celery -A config worker -l INFO
# celery -A config beat -l INFO
celery -A config worker --beat -l INFO
