#!/bin/bash
set -e
touch /opt/New_timer/log/gunicorn.log
touch /opt/New_timer/log/gunicorn.err
touch /opt/New_timer/log/access.log

# Start Gunicorn processes
echo Starting Gunicorn...
exec gunicorn manage:app \
        --bind 0.0.0.0:8000 \
        --workers 4 \
        --log-level=info \
        --log-file=/opt/New_timer/log/gunicorn.log \
        --access-logfile=/opt/New_timer/log/access.log \
        "$@"
echo Gunicorn is running...
