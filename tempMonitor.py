import socketio
import time
import datetime
import adafruit_dht
import board
import json

import obdUtils

SENSOR_TYPE = 'TEMP'
ERROR = 'ERR'
INFO = 'INFO'
RETRY_INTERVAL = 1 #Delay in seconds when retrying to connect to node server

METRIC_UNITS = False

dhtSensor = adafruit_dht.DHT22(board.D23, use_pulseio=False)

numTries = 1


def emitTempData():
    while True:
        temp = 0.0
        humidity = 0.0

        try:
            humidity = dhtSensor.humidity
            temp = dhtSensor.temperature
            
            if temp is not None and humidity is not None:
                if not METRIC_UNITS: #convert to fahrenheit
                    temp = format(((temp * 9.0) / 5.0) + 32.0, ".1f")

                data = {'temp': temp, 'humidity': humidity}
                sio.emit('cabinTempHumidity', json.dumps(data))
            
        except Exception as ex: #logs any errors encountered during reading of gps. Also allows program to pick back up if node server connection is lost
            errorLog = obdUtils.createLogMessage(ERROR, SENSOR_TYPE, type(ex).__name__, ex.args)
            print(errorLog)
            sio.emit('log', json.dumps(errorLog)) #will only work if exception is unrelated to node server connection
            continue
            
        time.sleep(2)
        


while True: #loop until a connection is made with the server instead of immediately exiting
    try:
        sio = socketio.Client()
        sio.connect('http://localhost:3000')
        emitTempData() #temp workaround. Originally not needed. Seems to be issue with nodejs socketio version not sending connect packet to trigger connect() event
        break
        
    except Exception as ex:
        errorLog = obdUtils.createLogMessage(ERROR, SENSOR_TYPE, type(ex).__name__, ex.args)
        print(errorLog)
        numTries += 1
        print("Temp app unable to connect to node server, retrying attempt {0}".format(numTries))
        time.sleep(RETRY_INTERVAL)
            
        continue



@sio.event
def connect():
    
    connectedLog = obdUtils.createLogMessage(INFO, SENSOR_TYPE, 'Connection', 'Established')
    print(connectedLog)
    sio.emit('log', json.dumps(connectedLog))
    
    emitTempData()
