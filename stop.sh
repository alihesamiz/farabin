supervisorctl -c supervisord.conf stop all
supervisorctl -c supervisord.conf shutdown

sudo kill -9 $(sudo lsof -t -i :8000)

echo "Supervisor stopped successfully!"
