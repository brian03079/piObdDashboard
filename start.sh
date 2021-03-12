#!/bin/bash
xterm -e "node index.js; bash" &
sleep 3
xterm -e "python3 tempMonitor.py; bash" &
xterm -e "python3 obdDash.py; bash" &
