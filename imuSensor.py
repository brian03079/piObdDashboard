import time
import json
import datetime
import math
import board
import adafruit_bno055
import socketio

import obdUtils

SENSOR_TYPE = 'IMU'
ERROR = 'ERR'
INFO = 'INFO'
RETRY_INTERVAL = 1 #Delay in seconds when retrying to connect to node server
POLL_INTERVAL = .0333333 #~30hz

GRAVITY = 9.80665
 
i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)
 
last_val = 0xFFFF

sio = None
numTries = 1


def temperature():
    global last_val  # pylint: disable=global-statement
    result = sensor.temperature
    if abs(result - last_val) == 128:
        result = sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result


def emitImuData():
    global i2c
    global sensor
                
    while True:
        
        try:
            xA, yA, zA = sensor.acceleration
            xL, yL, zL = sensor.linear_acceleration
            heading, roll, pitch = sensor.euler
            temp = temperature()
            xQ, yQ, zQ, wQ = sensor.quaternion
            sys, gyro, accel, mag = sensor.calibration_status
            
            data = {
                "accelX": xA,
                "accelY": yA,
                "accelZ": zA,
                "linAccelX": xL,
                "linAccelY": yL,
                "linAccelZ": zL,
                "gForce": math.sqrt((xL * xL) + (yL * yL) + (zL * zL)) / GRAVITY,
                "heading": heading,
                "roll": roll,
                "pitch": pitch,
                "temp": temp,
                "quatX": xQ, #quatX and quatY seem to be reversed? x and y values will be swapped in javascript
                "quatY": yQ,
                "quatZ": zQ,
                "quatW": wQ,
                "calSys": sys,
                "calGyro": gyro,
                "calAccel": accel,
                "calMag": mag,
            }
            
            sio.emit('imuData', json.dumps(data))
            
        except Exception as ex: 
                
                errorLog = obdUtils.createLogMessage(ERROR, SENSOR_TYPE, type(ex).__name__, ex.args)
                print(errorLog)
                sio.emit('log', json.dumps(errorLog)) #will only work if exception is unrelated to node server connection
                i2c = board.I2C() #try to reconnect to BNO055 sensor
                sensor = adafruit_bno055.BNO055_I2C(i2c)

                continue
     
        time.sleep(POLL_INTERVAL)
        
while True: #loop until a connection is made with the server instead of immediately exiting
    try:
        sio = socketio.Client()
        sio.connect('http://localhost:3000')
        emitImuData() #temp workaround. Originally not needed. Seems to be issue with nodejs socketio version not sending connect packet to trigger connect() event
        break;

    except Exception as ex:
        numTries += 1
        print("IMU app unable to connect to node server, retrying attempt {0}".format(numTries))
        errorLog = obdUtils.createLogMessage(ERROR, SENSOR_TYPE, type(ex).__name__, ex.args)
        print(errorLog)
        time.sleep(RETRY_INTERVAL)
            
        continue
        
@sio.event
def connect():
    
    connectedLog = obdUtils.createLogMessage(INFO, SENSOR_TYPE, 'Connection', 'Established')
    print(connectedLog)
    sio.emit('log', json.dumps(connectedLog))
    
    emitImuData()




