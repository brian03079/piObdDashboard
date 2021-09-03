# !/bin/python

import RPi.GPIO as GPIO
import time
import os
import socketio
import json
import datetime

import obdUtils

POLL_INTERVAL = 1 #seconds
RETRY_INTERVAL = 1 #Delay in seconds when retrying to connect to node server

 
# Use the Broadcom SOC Pin numbers
# Setup the pin with internal pullups enabled and pin in reading mode.
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)

sio = None
numTries = 1
    
#Send a simple ping that lets the dashcam python app know to toggle camera preview on/off
def toggleCameraPreview(channel):

    print("Toggling camera preview...")
    sio.emit('cameraPreviewToggle', 1) 

def shutdown(channel):

    print("Shutting Down")
    os.system("sudo shutdown -h now")

def restartApps(channel):

    print("Restarting apps...")
    os.system("/home/pi/piObdDashboard/restartApps.sh")
    
def pollSysInfo():
    
    diskUsage = obdUtils.getDiskUsage()
    cpuUsage = obdUtils.getCpuUsage()
    
    gpuTemp = obdUtils.getGpuTemp()
    cpuTemp = obdUtils.getCpuTemp()
    
    data = {
        'diskUsagePercent': diskUsage,
        'cpuUsagePercent': cpuUsage,
        'gpuTemp': cpuTemp,
        'cpuTemp': gpuTemp
    }
    
    sio.emit('sysInfoData', json.dumps(data))
    
def emitSysTemps():
    cpuTemp = int(obdUtils.runSysCmd(CPU_TEMP_CMD)) / 1000 #note the required division
    gpuTemp = re.search("\d+\.\d+", str(obdUtils.runSysCmd(GPU_TEMP_CMD))).group() #extract the decimal number using regular expression
       
    sysTempData = {
        "cpuTemp": cpuTemp,
        "gpuTemp": gpuTemp
    }
        
    print(sysTempData)
    sio.emit('sysTempData', json.dumps(sysTempData))
    
# Add our function to execute when the button pressed event happens
GPIO.add_event_detect(26, GPIO.FALLING, callback=toggleCameraPreview, bouncetime=2000) #toggle camera preview on/off
GPIO.add_event_detect(21, GPIO.FALLING, callback=shutdown, bouncetime=2000)
GPIO.add_event_detect(20, GPIO.FALLING, callback=restartApps, bouncetime=2000)

def startApp():
    while True:
        pollSysInfo()
        time.sleep(POLL_INTERVAL)
    
while True: #loop until a connection is made with the server instead of immediately exiting
    try:
        sio = socketio.Client()
        sio.connect('http://localhost:3000')
        startApp() #temp workaround. Originally not needed. Seems to be issue with nodejs socketio version not sending connect packet to trigger connect() event
        break
        
    except Exception as ex:
        errorLog = obdUtils.createLogMessage('asdf', 'asdf', type(ex).__name__, ex.args)
        print(errorLog)
        numTries += 1
        print("buttons app unable to connect to node server, retrying attempt {0}".format(numTries))
        time.sleep(RETRY_INTERVAL)
            
        continue


@sio.event
def connect():
    
    connectedLog = obdUtils.createLogMessage(INFO, SENSOR_TYPE, 'Connection', 'Established')
    print(connectedLog)
    sio.emit('log', json.dumps(connectedLog))
    
    startApp()
