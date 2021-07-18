#!/bin/bash
#terminate any associated apps in case this script is rerun as part of a restart for misbehaving apps
sudo killall gpsd node python3 
sudo gpsd /dev/serial0 -F /var/run/gpsd.sock #enable gpsd daemon for helping to parse gps data

#start the apps
cd /home/pi/piObdDashboard
/home/pi/.config/nvm/versions/node/v14.16.0/bin/node index.js & #need to manually specify installation dir if node was installed by nvm
sleep 2 #give enough time for node server to start
python3 tempMonitor.py &
#python3 obdDash.py &
python3 imuSensor.py &
python3 gpsModule.py &
python3 airSensor.py &
