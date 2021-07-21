# !/bin/python

import RPi.GPIO as GPIO
import time
import threading
import os
import subprocess
import socketio
import json
import datetime

POLL_INTERVAL = 1
 
# Use the Broadcom SOC Pin numbers
# Setup the pin with internal pullups enabled and pin in reading mode.
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    
#Send a simple ping that lets the web app know to toggle camera preview on/off
def toggleCameraPreview(channel):

    print("Toggling camera preview...")
    sio.emit('cameraPreviewToggle', 1) 

def shutdown(channel):

    print("Shutting Down")
    time.sleep(5)
    os.system("sudo shutdown -h now")

def restartApps(channel):

    print("Restarting apps...")
    os.system("/home/pi/piObdDashboard/restartApps.sh")

# Add our function to execute when the button pressed event happens
GPIO.add_event_detect(26, GPIO.FALLING, callback=restartApps, bouncetime=2000) #toggle camera preview on/off
GPIO.add_event_detect(21, GPIO.FALLING, callback=shutdown, bouncetime=2000)
GPIO.add_event_detect(20, GPIO.FALLING, callback=restartApps, bouncetime=2000)

while True:
    time.sleep(POLL_INTERVAL)
