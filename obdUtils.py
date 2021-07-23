import time
import socketio
import json
import datetime
import subprocess

def createLogMessage(logType, sensor, description, detailedDescription):
    now = datetime.datetime.now()
    timestamp = "%d:%d:%d" % (now.hour, now.minute, now.second)
            
    return {
        'logType': logType,
        'sensor' : sensor,
        'exType' : description,
        'args' : detailedDescription,
        'timeStamp': timestamp
    }

def formatDecimalPlaces(dec, numPlaces):
    formatPlaces = "{:." + str(numPlaces) + "f}"
    
    return formatPlaces.format(dec)

    
def runSysCmd(cmdString):
    proc = subprocess.Popen([cmdString], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    
    return out
