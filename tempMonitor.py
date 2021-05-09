import socketio
import time
import adafruit_dht
import board
import json

METRIC_UNITS = False

dhtSensor = adafruit_dht.DHT22(board.D23, use_pulseio=False)

sio = socketio.Client()
sio.connect('http://localhost:3000')


@sio.event
def message(data):
    print('I received a message!')

@sio.on('my message')
def on_message(data):
    print('I received a message!')

while True:
    temp = 0.0
    humidity = 0.0
    
    try:
        humidity = dhtSensor.humidity
        temp = dhtSensor.temperature
    except RuntimeError:
        print("RuntimeError, trying again...")
        continue

    if temp is not None and humidity is not None:
        if not METRIC_UNITS: #convert to fahrenheit
            temp = format(((temp * 9.0) / 5.0) + 32.0, ".1f")

        data = {'temp': temp, 'humidity': humidity}
        print(data)
        sio.emit('cabinTempHumidity', json.dumps(data))
    
    time.sleep(3)
