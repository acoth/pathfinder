#!/bin/sh
which python
PID1=`pgrep -f serveOdds.py`
if [ -z "$PID1" ]; then
    echo "Web server not running"
else
    echo "Web server running; restarting..."
    kill $PID1
fi
python serveOdds.py 2>flaskLog -p $1 &

