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


currentDtcCodes = []
dtcCodesChanged = False

connection = obd.OBD()

while not obd.is_connected():
    print("Initial OBD connection failed. Retrying.")
    sleep(1);
    connection = obd.OBD()
    
print("OBD connection established!")

sio = socketio.Client()
sio.connect('http://localhost:3000')

def emitBaseTelemetry():
    
    speedCmd = obd.commands.SPEED # select an OBD command (sensor)
    response = connection.query(speedCmd) # send the command, and parse the response
    speed = str(response.value.to("mph").magnitude)
    
    rpmCmd = obd.commands.RPM
    response = connection.query(rpmCmd)
    rpm = response.value.magnitude
    
    throttleCmd = obd.commands.THROTTLE_POS
    response = connection.query(throttleCmd)
    throttle = str(response.value.magnitude)
    
    data = {'speed': speed, 'rpm': rpm, 'throttle': throttle}
    sio.emit('data', json.dumps(data))

def emitDtcCodes():
    
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

@sio.on('my message')
def on_message(data):
    print('I received a message!')

@sio.event
def connect():
    print("Connected to node server!")

    while (True):
        try:
            emitBaseTelemetry()
            emitDtcCodes()
            
            time.sleep(.3) #fastest refresh speed before web app begins to lag
        except:
            print("No connection to car. Attempting reconnect.")
            time.sleep(1)
            connection = obd.OBD()
            

#attempt to reconnect on connection error
@sio.event
def connect_error():
    print("Node server connect failed. Retrying.")
    time.sleep(3)
    sio.connect('http://localhost:3000')

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.event
def message(data):
    print('I received a message!')
