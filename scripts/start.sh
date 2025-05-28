#!/bin/bash


source env.sh


if ! command -v supervisord &>/dev/null; then
    echo "Supervisor is not installed. Attempting to install..."
    sudo apt update
    if sudo apt install -y supervisor; then
        echo "Supervisor installed successfully."
        if command -v supervisord &>/dev/null; then
            echo "Supervisord found in PATH."
        else
            echo "Warning: Supervisord not found in PATH after installation. Check your system's PATH configuration."
        fi
    else
        echo "Error: Failed to install Supervisor. Please check the output for errors."
        exit 1
    fi
fi

stop.sh

supervisord -c supervisord.conf

supervisorctl -c supervisord.conf status

echo "Supervisor setup and started successfully!"
