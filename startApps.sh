#!/bin/bash
sleep 2 #give enough time to go to desktop
stty -F /dev/serial0 raw 9600 cs8 clocal -cstopb #ready the serial port for reading from Adafruit Ultimate GPS HAT
sudo gpsd /dev/serial0 -F /var/run/gpsd.sock
#start the apps
cd /home/pi/piObdDashboard
/home/pi/.config/nvm/versions/node/v14.16.0/bin/node index.js & #need to manually specify installation dir if node was installed by nvm
sleep 2 #give enough time for node server to start
python3 tempMonitor.py &
#python3 obdDash.py &
python3 imuSensor.py &
python3 gpsModule.py &
python3 airSensor.py &
python buttons.py & #use python instead of python3 so it wont be terminated on restartApps.sh
#chromium-browser --window-position=0,0 --kiosk
#unclutter -idle 1 &
