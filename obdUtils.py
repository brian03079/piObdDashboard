import time
import socketio
import json
import datetime
import psutil
import re
import os
import subprocess

CPU_TEMP_CMD = 'cat /sys/class/thermal/thermal_zone0/temp' #Celcius. Needs to be divided by 1000
GPU_TEMP_CMD = "vcgencmd measure_temp" #Celcius. Returned output is format of "temp=53.5'C"

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

def getDiskUsage():
    return psutil.disk_usage("/").percent

def getCpuUsage():
	return str(psutil.cpu_percent())

def getCpuTemp():
    return int(runSysCmd(CPU_TEMP_CMD)) / 1000 #note the required division
    
def getGpuTemp():
    return re.search("\d+\.\d+", str(runSysCmd(GPU_TEMP_CMD))).group() #extract the decimal number using regular expression
