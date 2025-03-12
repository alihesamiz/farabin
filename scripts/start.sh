#!/bin/bash


source env.sh

if ! command -v supervisord &>/dev/null; then
    echo "Supervisor is not installed. Installing..."
    sudo apt install -y supervisor
fi

stop.sh

supervisord -c supervisord.conf

supervisorctl -c supervisord.conf status

echo "Supervisor setup and started successfully!"
