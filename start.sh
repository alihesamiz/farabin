#!/bin/bash

if ! command -v supervisord &>/dev/null; then
    echo "Supervisor is not installed. Installing..."
    sudo apt install -y supervisor
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

if ! [ -f "$SCRIPT_DIR/logs" ]; then
    mkdir "$SCRIPT_DIR/logs"
    echo "Logs directory created."
fi

bash "$SCRIPT_DIR/stop.sh"

supervisord -c supervisord.conf

supervisorctl -c supervisord.conf status

echo "Supervisor setup and started successfully!"
