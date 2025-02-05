#!/bin/bash

# Install Supervisor
sudo apt install -y supervisor

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if .env exists in the script directory
if [ -f "$SCRIPT_DIR/.env" ]; then
    echo "Loading environment variables from .env file in $SCRIPT_DIR..."
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
    echo "Done Loading..."
else
    echo "No .env file found in $SCRIPT_DIR."
    exit 1
fi

# Shutdown any existing Supervisor instance (if running)
supervisorctl -c supervisord.conf stop all
supervisorctl -c supervisord.conf shutdown

sudo kill -9 $(sudo lsof -t -i :8000)

# Start Supervisor with the specified configuration file
supervisord -c supervisord.conf

supervisorctl -c supervisord.conf status

echo "Supervisor setup and started successfully!"
