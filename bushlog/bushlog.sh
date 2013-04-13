#!/bin/sh

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DESC="Guncorn Startup"
NAME=$(basename $0)
SCRIPTNAME=/etc/init.d/$NAME

ROOT=/opt/bushlog
BIN_PATH=$ROOT/bin
LOG_PATH=/var/log/gunicorn
CONTROLSCRIPT=$BIN_PATH/gunicorn_django
PIDFILE=/tmp/$NAME.pid
HOST=127.0.0.1
PORT=8000
WORKERS=3
RUN_AS=bushlog

d_start(){
    if [ -f $PIDFILE ]; then
        echo -n " already running"
    else
        start-stop-daemon --start --quiet \
            --pidfile $PIDFILE \
            --chuid $RUN_AS \
            --exec $CONTROLSCRIPT \
            bind=$HOST:$PORT \
            workers=$WORKERS \
            log-file=$LOG_PATH/bushlog.log \
            pid=$PIDFILE
            daemon
        chmod 400 $PIDFILE
    fi
}

d_stop(){
    start-stop-daemon --stop --quiet --pidfile $PIDFILE \
            || echo -n " not running"
    if [ -f $PIDFILE ]; then
        rm $PIDFILE
    fi
}


case $1 in
    start)
    echo -n "Starting $DESC: $NAME"
    d_start
    echo "."
    ;;
    stop)
    echo -n "Stopping $DESC: $NAME"
    d_stop
    echo "."
    ;;
    restart)
    echo -n "Restarting: $DESC: $NAME"
    d_stop
    sleep 1
    d_start
    echo "."
    ;;
    *)
    echo "Usage: $0 (start|stop|restart)"
    exit 1
    ;;
esac
