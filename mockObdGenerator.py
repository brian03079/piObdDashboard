import socketio
import random 
import time
import json
import obd
import time

obd2CmdListFile = open('obd2CmdsList.json',) 
obdCmdList = json.load(obd2CmdListFile)

obd2CmdListFile.close()


sio = socketio.Client()

sio.connect('http://localhost:3000')

def generateFaultCodes():
    return [
        ("P0104", "Mass or Volume Air Flow Circuit Intermittent"),
        ("B0003", ""), # unknown error code, it's probably vehicle-specific
        ("C0123", "")
        ]
    
def generateData():
    idleTime = round(random.uniform(10.5, 75.5), 1)
    print(idleTime)

    data = {'speed': random.randint(75, 85),
        'rpm': random.randint(700, 7500),
        'throttle': random.randint(40, 60),
        'runTime': random.randint(60, 90),
        'idleTime': idleTime}
        
    return json.dumps(data)

def sendData():
    sio.emit('data', generateData())
    sio.emit('dtcData', generateFaultCodes())
    time.sleep(1)

@sio.on('sensorDumpRequest')
def on_message(data):
    
    obdCmdResponseList = []

    for obdCmd in obdCmdList: 
        #response = connection.query(obdCmd['Name']) # send the command, and parse the response
        
        obdCmdResponseList.append(obdCmd)

    sio.emit('sensorDumpData', obdCmdResponseList)

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
