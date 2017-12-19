#!/bin/sh
cd /home/pi/pathfinder/

pgrep -a python | grep serveOdds.py > /dev/null
if [ $? -eq 0 ]; then
    echo "Web server is already running."
else
    python serveOdds.py 2>flaskLogPath &
fi

