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




sio = socketio.Client()

sio.connect('http://localhost:3000')

@sio.on('my message')
def on_message(data):
    print('I received a message!')

@sio.event
def connect():
    print("Connected!")
    connection = obd.OBD() # auto-connects to USB or RF port

    while (True):
        speedCmd = obd.commands.SPEED # select an OBD command (sensor)
        response = connection.query(speedCmd) # send the command, and parse the response
        speed = str(response.value.to("mph").magnitude)
        
        rpmCmd = obd.commands.RPM # select an OBD command (sensor)
        response = connection.query(rpmCmd) # send the command, and parse the response
        rpm = response.value.magnitude
        
        throttleCmd = obd.commands.THROTTLE_POS # select an OBD command (sensor)
        response = connection.query(throttleCmd) # send the command, and parse the response
        throttle = str(response.value.magnitude)

        data = {'speed': speed, 'rpm': rpm, 'throttle': throttle}
        sio.emit('data', json.dumps(data))
        time.sleep(.25)
        #print(response.value) # returns unit-bearing values thanks to Pint
        #print(response.value.to("mph"), end="\r", flush=True) # user-friendly unit conversions
    
    #while (True):
    #logData()

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.event
def message(data):
    print('I received a message!')
