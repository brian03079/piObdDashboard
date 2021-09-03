#!/bin/bash
stty -F /dev/serial0 raw 9600 cs8 clocal -cstopb #ready the serial port for reading from Adafruit Ultimate GPS HAT
sudo gpsd /dev/serial0 -F /var/run/gpsd.sock

cd /home/pi/piObdDashboard

#start the apps
/home/pi/.nvm/versions/node/v16.8.0/bin/node index.js & #need to manually specify installation dir if node was installed by nvm

python3 tempMonitor.py &
python3 obdDash.py &
python3 imuSensor.py &
python3 gpsModule.py &
python3 airSensor.py &
python3 obdMisc.py & #use python instead of python3 so it wont be terminated on restartApps.sh

cd /home/pi/piDashcam
sudo python3 dashcam.py &

chromium-browser --window-position=0,0    --kiosk --user-data-dir="/home/pi/Documents/Profiles/0" http://localhost:3000 &
chromium-browser --window-position=600,0    --kiosk --user-data-dir="/home/pi/Documents/Profiles/1" http://localhost:3000/misc &

unclutter -idle 1 &
