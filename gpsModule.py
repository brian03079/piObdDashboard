import time
import socketio
import json
import datetime
from gps import *

#see https://gpsd.gitlab.io/gpsd/gpsd_json.html for more details on getting data from gpsd

SENSOR_TYPE = 'GPS'
delay = 1 #gps polling interval in seconds. Max polling rate 10hz for Adafruit Ultimate GPS (MTK3339 chipset)
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 

sio = socketio.Client()
sio.connect('http://localhost:3000')

def formatDecimalPlaces(dec, numPlaces):
    formatPlaces = "{:." + str(numPlaces) + "f}"
    return formatPlaces.format(dec)

def emitGpsData():
    while True:
        time.sleep(delay)
     
        try:
            report = gpsd.next()

            if report['class'] == 'TPV': #time-position-velocity report object
                data = {
                    'latitude': formatDecimalPlaces(getattr(report,'lat',0.0), 5),
                    'longitude': formatDecimalPlaces(getattr(report,'lon',0.0), 5),
                    'time': getattr(report,'time',''), #Time/date stamp in ISO8601 format, UTC. May have a fractional part of up to .001sec precision. May be absent if the mode is not 2D or 3D.
                    'altitude': getattr(report,'alt','nan'),#Altitude, height above ellipsoid, in meters. Probably WGS84.
                    'speed': formatDecimalPlaces((getattr(report,'speed',0.0) * 2.2369), 2), #mph converted from meters per second
                    'climb': getattr(report,'climb','nan'), #Climb (positive) or sink (negative) rate, meters per second.
                    'latitudeErr': getattr(report,'epy','nan'), #Latitude error estimate in meters. Certainty unknown.
                    'longitudeErr': getattr(report,'epx','nan'), #Longitude error estimate in meters. Certainty unknown.
                    'timeErr': getattr(report,'ept','nan'), #Estimated time stamp error in seconds. Certainty unknown.
                    'altitudeErr': getattr(report,'epv','nan'), #Estimated vertical error in meters. Certainty unknown.
                    'speedErr': getattr(report,'eps','nan'),#Estimated speed error in meters per second. Certainty unknown.
                    'climbErr': getattr(report,'epc','nan') #Estimated climb error in meters per second. Certainty unknown.
                }
                    
                sio.emit('gpsData', json.dumps(data))
                
        except Exception as ex:
            print("Unable to read from gps sensor, retrying...")
            
            now = datetime.datetime.now()
            timestamp = "%d-%d-%d_%d_%d_%d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)

            template = "Exception: {0} occurred. Args:{1!r}"
            errorDesc = template.format(type(ex).__name__, ex.args)
            
            error = {
                'sensor' : SENSOR_TYPE,
                'description': errorDesc,
                'timeStamp': timestamp
            }
            print(error)
            sio.emit('error', error)
            continue


@sio.event
def connect():
    print("Gps connected to node server!")
    emitGpsData()
   
