# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
 
"""
Example sketch to connect to PM2.5 sensor with either I2C or UART.
"""
 
# pylint: disable=unused-import
import socketio
import json
import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C
 
 
reset_pin = None
# If you have a GPIO, its not a bad idea to connect it to the RESET pin
# reset_pin = DigitalInOut(board.G0)
# reset_pin.direction = Direction.OUTPUT
# reset_pin.value = False
 
 
# For use with a computer running Windows:
# import serial
# uart = serial.Serial("COM30", baudrate=9600, timeout=1)
 
# For use with microcontroller board:
# (Connect the sensor TX pin to the board/computer RX pin)
# uart = busio.UART(board.TX, board.RX, baudrate=9600)
 
# For use with Raspberry Pi/Linux:
# import serial
# uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
 
# For use with USB-to-serial cable:
# import serial
# uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=0.25)
 
# Connect to a PM2.5 sensor over UART
# from adafruit_pm25.uart import PM25_UART
# pm25 = PM25_UART(uart, reset_pin)
 
# Create library object, use 'slow' 100KHz frequency!
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Connect to a PM2.5 sensor over I2C
pm25 = PM25_I2C(i2c, reset_pin)

sio = socketio.Client()
sio.connect('http://localhost:3000')

delay = 1 #sensor polling interval in seconds. Max polling rate 1s for PMSA003I 


def emitAirSensorData():
    while True:
        time.sleep(delay)
     
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
        except RuntimeError:
            print("Unable to read from sensor, retrying...")
            sio.emit('airQualityError', 1)
            continue


@sio.event
def connect():
    print("Air sensor connected to node server!")

    emitAirSensorData()

