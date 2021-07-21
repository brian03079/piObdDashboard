import socketio
import random 
import time
import json
import obd
import time
import re
import plotly.graph_objs as go 
from collections import deque 
from obd import OBDStatus

SENSOR_TYPE = 'OBD'
ERROR = 'ERR'


delay = 0.3 #Delay in seconds before sending data

idleTime = 0.0 #Time the engine is idling in seconds
maxIdleRpm = 1000 #rpm threshold that helps define if engine is idling
maxThrottleActuatorIdle = 2.5

currentDtcCodes = []
dtcCodesChanged = False

def createLogMessage(ex, logType, sensor):
    now = datetime.datetime.now()
    timestamp = "%d:%d:%d" % (now.hour, now.minute, now.second)
            
    return {
        'logType': ERROR,
        'sensor' : SENSOR_TYPE,
        'exType' : type(ex).__name__,
        'args' : ex.args,
        'timeStamp': timestamp
    }


numTries = 1

def emitDtcCodes():
    
    global dtcCodesChanged
    dtcCmd = obd.commands.GET_DTC
    response = connection.query(dtcCmd)
    dtcCodes = response.value
    
    for i in dtcCodes: #add new codes if they don't exist
        dtcCodesChanged = True
        if dtcCodes[i] not in currentDtcCodes:
            currentDtcCodes.append(dtcCodes[i])
            
    for i in currentDtcCodes: #remove any codes that were resolved
        dtcCodesChanged = True
        if (currentDtcCodes[i] not in dtcCodes):
            currentDtcCodes.pop(i)
                    
    if dtcCodesChanged:
        sio.emit('dtcData', currentDtcCodes())
        dtcCodesChanged = False

def emitTelemetry():
    global idleTime
    
    while True:
        try:
            speedCmd = obd.commands.SPEED # select an OBD command (sensor)
            response = connection.query(speedCmd) # send the command, and parse the response
            speed = str(response.value.to("mph").magnitude)
            
            rpmCmd = obd.commands.RPM
            response = connection.query(rpmCmd)
            rpm = response.value.magnitude
            
            throttleCmd = obd.commands.THROTTLE_POS
            response = connection.query(throttleCmd)
            throttle = str(response.value.magnitude)
            
            runTimeCmd = obd.commands.RUN_TIME
            response = connection.query(runTimeCmd)
            runTime = str(response.value)
            
            throttleActuatorCmd = obd.commands.THROTTLE_ACTUATOR # less than 2.5% at idle
            response = connection.query(throttleActuatorCmd)
            throttleActuator = response.value.magnitude
            
            if (speed < .1):
                idleTime += delay
            
            data = {'speed': speed, 'rpm': rpm, 'throttle': throttle, 'runTime': runTime, 'idleTime': idleTime}
            sio.emit('data', json.dumps(data))
            
            emitDtcCodes()
            
            time.sleep(.3)
            
        except Exception as ex: #logs any errors encountered during reading of gps. Also allows program to pick back up if node server connection is lost
            errorLog = createLogMessage(ERROR, SENSOR_TYPE, type(ex).__name__, ex.args)
            print(errorLog)
            sio.emit('log', json.dumps(errorLog)) #will only work if exception is unrelated to node server connection
            continue


while True: #loop until a connection is made with the server instead of immediately exiting
    try:
        connection = obd.OBD()
        print("OBD connection established!")
        
        sio = socketio.Client()
        sio.connect('http://localhost:3000')
        emitTelemetry()
        
    except Exception as ex:
        numTries += 1
        print("Unable to connect to node server, retrying attempt {0}".format(numTries))
        time.sleep(1)
            
        continue
        


@sio.event
def connect():
    print("Connected to node server!")
    emitTelemetry()

