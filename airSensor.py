import socketio
import json
import time
import datetime
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C
 
 
reset_pin = None
SENSOR_TYPE = 'AIR'
ERROR = 'ERR'

DELAY = 1 #sensor polling interval in seconds. Max polling rate 1s for PMSA003I 

 
# Create library object, use 'slow' 100KHz frequency!
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Connect to a PM2.5 sensor over I2C
pm25 = PM25_I2C(i2c, reset_pin)
sio = None


numTries = 1
while True: #loop until a connection is made with the server instead of immediately exiting
    try:
        sio = socketio.Client()
        sio.connect('http://localhost:3000')
        
        break
    except Exception as ex:
        numTries += 1
        print("Unable to connect to node server, retrying attempt {0}".format(numTries))
        time.sleep(1)
            
        continue

def createLogMessage(ex, logType, sensor):
    now = datetime.datetime.now()
    timestamp = "%d:%d:%d" % (now.hour, now.minute, now.second)
            
    return {
        'logType': ERROR,
        'sensor' : SENSOR_TYPE,
        'exType' : type(ex).__name__,
        'args' : ex.args,
        'timeStamp': timestamp
    }

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
            errorLog = createLogMessage(ex, ERROR, SENSOR_TYPE)
            print(errorLog)
            sio.emit('log', json.dumps(errorLog))
            continue


@sio.event
def connect():
    print("Air sensor connected to node server!")
    emitAirSensorData()

