#!/bin/bash
# Remove any existing crond.pid file
rm -f /var/run/crond.pid

# Ensure proper permissions for /var/run
chmod 755 /var/run

# Start cron
service cron start

# Log cron service status
service cron status >> /var/log/cron.log

# Start Flask application
python /app/app.py
