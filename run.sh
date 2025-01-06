#!/bin/bash

# Install Supervisor
sudo apt install -y supervisor

# Shutdown any existing Supervisor instance (if running)
supervisorctl -c supervisord.conf shutdown

# Start Supervisor with the specified configuration file
supervisord -c supervisord.conf

supervisorctl -c supervisord.conf status

echo "Supervisor setup and started successfully!"