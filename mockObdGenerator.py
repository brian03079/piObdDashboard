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

def generateFaultCodes():
    return [
        ("P0104", "Mass or Volume Air Flow Circuit Intermittent"),
        ("B0003", ""), # unknown error code, it's probably vehicle-specific
        ("C0123", "")
        ]
    
def generateData():
    
    data = {'speed': random.randint(75, 85),
        'rpm': random.randint(1500, 5000),
        'throttle': random.randint(40, 60)}
    return json.dumps(data)

def sendData():
    sio.emit('data', generateData())
    sio.emit('faultCodeData', generateFaultCodes())
    time.sleep(.2)

@sio.on('my message')
def on_message(data):
    print('I received a message!')

@sio.event
def connect():
    print("Connected!")

    while (True):
        generateFaultCodes()
        sendData()

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.event
def message(data):
    print('I received a message!')
