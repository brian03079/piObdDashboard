import time
import socketio
import json
import datetime
import board
import adafruit_bno055
 
SENSOR_TYPE = 'IMU'
ERROR = 'ERR'
POLL_INTERVAL = .0333333
 
i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)
 
last_val = 0xFFFF

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

def createLogMessage(logType, sensorType, ex, args):
    now = datetime.datetime.now()
    timeStamp = "%d:%d:%d" % (now.hour, now.minute, now.second)
            
    return {
        'logType': logType,
        'sensor' : sensorType,
        'exType' : ex, #pass empty string if not exception
        'args' : args,
        'timeStamp': timeStamp
    }
 
 
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
            if (roll is not None):
                #print(data)
                sio.emit('imuData', json.dumps(data))
            
        except Exception as ex: #logs any errors encountered during reading of gps. Also allows program to pick back up if node server connection is lost
                
                errorLog = createLogMessage(ERROR, SENSOR_TYPE, type(ex).__name__, ex.args)
                print(errorLog)
                sio.emit('log', json.dumps(errorLog)) #will only work if exception is unrelated to node server connection
                i2c = board.I2C()
                sensor = adafruit_bno055.BNO055_I2C(i2c)

                continue
     
        time.sleep(POLL_INTERVAL)

@sio.event
def connect():
    print("IMU connected to node server!")
    emitImuData()
