import dash 
from dash.dependencies import Output, Input
import dash_core_components as dcc 
import dash_html_components as html 
import plotly 
import socketio
import random 
import time
import plotly.graph_objs as go 
from collections import deque 

sio = socketio.Client()

sio.connect('http://localhost:3000')

def randomData():
    return random.randint(0, 60)

def logData():
    sio.emit('data', randomData())
    time.sleep(.15)


@sio.on('my message')
def on_message(data):
    print('I received a message!')

@sio.event
def connect():
    print("I'm connected!")
    while (True):
        logData()

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.event
def message(data):
    print('I received a message!')
