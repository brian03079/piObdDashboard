#!/bin/bash
#terminate any associated apps in case this script is rerun as part of a restart for misbehaving apps
sudo killall gpsd node python3 python
pkill -o chromium
sudo gpsd /dev/serial0 -F /var/run/gpsd.sock #enable gpsd daemon for helping to parse gps data

cd /home/pi/piObdDashboard #dir of all the apps to run

#start the apps
/home/pi/.nvm/versions/node/v16.8.0/bin/node index.js & #need to manually specify installation dir if node was installed by nvm

python3 tempMonitor.py &
python3 obdDash.py &
python3 imuSensor.py &
python3 gpsModule.py &
python3 airSensor.py &
python3 obdMisc.py &

cd /home/pi/piDashcam
sudo python3 dashcam.py &

chromium-browser --window-position=0,0    --kiosk --user-data-dir="/home/pi/Documents/Profiles/0" http://localhost:3000 &
chromium-browser --window-position=600,0    --kiosk --user-data-dir="/home/pi/Documents/Profiles/1" http://localhost:3000/misc &
