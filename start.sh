#!/bin/bash
cd /home/pi/piObdDashboard
sleep 2
/home/pi/.config/nvm/versions/node/v14.16.0/bin/node index.js & #need to manually specify installation dir if node was installed by nvm
sleep 4 #give enough time for node server to start
python3 tempMonitor.py &
python3 obdDash.py &
chromium-browser --window-position=0,0 --kiosk
unclutter -idle 1 &
