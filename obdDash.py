import dash 
from dash.dependencies import Output, Input
import dash_core_components as dcc 
import dash_html_components as html 
import plotly 
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

connection = obd.OBD()

while not obd.is_connected():
    print(Initial OBD connection failed. Retrying.")
    sleep(1);
    connection = obd.OBD()
    
print("OBD connection established!")

sio = socketio.Client()
sio.connect('http://localhost:3000')

@sio.on('my message')
def on_message(data):
    print('I received a message!')

@sio.event
def connect():
    print("Connected to node server!")

    while (True):
        try:
            speedCmd = obd.commands.SPEED # select an OBD command (sensor)
            response = connection.query(speedCmd) # send the command, and parse the response
            speed = str(response.value.to("mph").magnitude)
            
            rpmCmd = obd.commands.RPM # select an OBD command (sensor)
            response = connection.query(rpmCmd) # send the command, and parse the response
            rpm = response.value.magnitude
            
            throttleCmd = obd.commands.THROTTLE_POS # select an OBD command (sensor)
            response = connection.query(throttleCmd) # send the command, and parse the response
            throttle = str(response.value.magnitude)
            
            dtcCmd = obd.commands.GET_DTC # select an OBD command (sensor)
            response = connection.query(dtcCmd) # send the command, and parse the response
            dtcCodes = response.value

            data = {'speed': speed, 'rpm': rpm, 'throttle': throttle}
            sio.emit('data', json.dumps(data))
            time.sleep(.3)
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
