#! /bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo $SCRIPT_DIR

if [ -f "$SCRIPT_DIR/.env" ]; then
    echo "Loading environment variables from .env file..."
    set -a
    source "$SCRIPT_DIR/.env"
    set +a
    echo "Environment variables loaded."
else
    echo "No .env file found in $SCRIPT_DIR."
    exit 1
fi
