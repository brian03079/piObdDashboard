import socketio
import json
import time
import datetime
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C
 
import obdUtils
 
RESET_PIN = None
SENSOR_TYPE = 'AIR'
ERROR = 'ERR'
INFO = 'INFO'

RETRY_INTERVAL = 1 #Delay in seconds when retrying to connect to node server

DELAY = 1 #sensor polling interval in seconds. Max polling rate 1s for PMSA003I 

 
# Create library object, use 'slow' 100KHz frequency!
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Connect to a PM2.5 sensor over I2C
pm25 = PM25_I2C(i2c, RESET_PIN)

sio = None
numTries = 1


def emitAirSensorData():
    while True:
        time.sleep(DELAY)
     
        try:
            aqdata = pm25.read()
            
            data = {'pm10': aqdata["pm10 standard"],
                    'pm25': aqdata["pm25 standard"],
                    'pm100': aqdata["pm100 standard"],
                    'pm3um': aqdata["particles 03um"],
                    'pm5um': aqdata["particles 05um"],
                    'pm10um': aqdata["particles 10um"],
                    'pm25um': aqdata["particles 25um"],
                    'pm50um': aqdata["particles 50um"],
                    'pm100um': aqdata["particles 100um"]}

            sio.emit('airQualityData', json.dumps(data))
        except Exception as ex:
            errorLog = obdUtils.createLogMessage(ERROR, SENSOR_TYPE, type(ex).__name__, ex.args)
            print(errorLog)
            sio.emit('log', json.dumps(errorLog))
            continue

while True: #loop until a connection is made with the server instead of immediately exiting
    try:
        sio = socketio.Client()
        sio.connect('http://localhost:3000')
        emitAirSensorData() #temp workaround. Originally not needed. Seems to be issue with nodejs socketio version not sending connect packet to trigger connect() event
        break
        
    except Exception as ex:
        numTries += 1
        print("Unable to connect to node server, retrying attempt {0}".format(numTries))
        time.sleep(RETRY_INTERVAL)
            
        continue


@sio.event
def connect():
    connectedLog = obdUtils.createLogMessage(INFO, SENSOR_TYPE, 'Connection', 'Established')
    print(connectedLog)
    sio.emit('log', json.dumps(connectedLog))
    
    emitAirSensorData()
