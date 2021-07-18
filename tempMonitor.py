import socketio
import time
import datetime
import adafruit_dht
import board
import json

SENSOR_TYPE = 'TEMP'
ERROR = 'ERR'
INFO = 'INFO'
METRIC_UNITS = False

dhtSensor = adafruit_dht.DHT22(board.D23, use_pulseio=False)

numTries = 1
while True: #loop until a connection is made with the server instead of immediately exiting
    try:
        sio = socketio.Client()
        sio.connect('http://localhost:3000')
        
        break
    except Exception as ex:
        numTries += 1
        print("Temp app unable to connect to node server, retrying attempt {0}".format(numTries))
        time.sleep(1)
            
        continue
        
def createLogMessage(logType, sensor, description, detailedDescription):
    now = datetime.datetime.now()
    timestamp = "%d:%d:%d" % (now.hour, now.minute, now.second)
            
    return {
        'logType': logType,
        'sensor' : SENSOR_TYPE,
        'exType' : description,
        'args' : detailedDescription,
        'timeStamp': timestamp
    }


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
                print(data)
                sio.emit('cabinTempHumidity', json.dumps(data))
            
        except Exception as ex: #logs any errors encountered during reading of gps. Also allows program to pick back up if node server connection is lost
            errorLog = createLogMessage(ERROR, SENSOR_TYPE, type(ex).__name__, ex.args)
            print(errorLog)
            sio.emit('log', json.dumps(errorLog)) #will only work if exception is unrelated to node server connection
            continue
            
        time.sleep(3)
    
@sio.event
def connect():
    
    connectedLog = createLogMessage(INFO, SENSOR_TYPE, 'Connection', 'Established')
    print(connectedLog)
    sio.emit('log', json.dumps(connectedLog))
    
    emitTempData()
