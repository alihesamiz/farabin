#! /bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/.env" ]; then
    echo "Loading environment variables from .env file in $SCRIPT_DIR..."
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
    echo "Done Loading..."
else
    echo "No .env file found in $SCRIPT_DIR."
    exit 1
fi

celery -A config worker --beat -l INFO
