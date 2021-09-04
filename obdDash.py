import socketio
import random 
import time
import json
import obd
import obdUtils
import time
import re

SENSOR_TYPE = 'OBD'
ERROR = 'ERR'
RETRY_INTERVAL = 1 #Delay in seconds when retrying to connect to node server

delay = 0.3 #Delay in seconds before sending data. This can be decreased, but .3s seems to be the fastest
            #that the pi can display on the web dashboard. Otherwise the web page updating begins lagging

idleTime = 0.0 #Time the engine is idling in seconds

currentDtcCodes = []
dtcCodesChanged = False

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
            
            if (float(speed) < .1):
                idleTime += delay
            
            data = {'speed': speed, 'rpm': rpm, 'throttle': throttle, 'runTime': runTime, 'idleTime': idleTime}
            sio.emit('data', json.dumps(data))
            
            emitDtcCodes()
            
            time.sleep(delay)
            
        except Exception as ex: #logs any errors
            errorLog = obdUtils.createLogMessage(ERROR, SENSOR_TYPE, type(ex).__name__, ex.args)
            print(errorLog)
            sio.emit('log', json.dumps(errorLog)) #will only work if exception is unrelated to node server connection
            continue

connection = obd.OBD()

while True: #loop until a connection is made with the server instead of immediately exiting
    try:
        print("OBD connection established!")
        
        sio = socketio.Client()
        sio.connect('http://localhost:3000')
        emitTelemetry()
        break;
    except Exception as ex: 
            errorLog = obdUtils.createLogMessage(ERROR, SENSOR_TYPE, type(ex).__name__, ex.args)
            print(errorLog)
            sio.emit('log', json.dumps(errorLog)) #will only work if exception is unrelated to node server connection
            sleep(RETRY_INTERVAL)
            continue
        


@sio.event
def connect():
    print("Connected to node server!")
    emitTelemetry()

