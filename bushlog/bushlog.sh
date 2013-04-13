#!/bin/sh

echo "Restarting the gunicorn instance..."
kill -9 `cat /tmp/bushlog.pid`
sleep 5
./bin/gunicorn_django \
    --workers=3 \
    --max-requests=250 \
    --daemon \
    --log-file=/var/log/gunicorn/bushlog.log \
    --pid=/tmp/bushlog.pid
echo "Done."

