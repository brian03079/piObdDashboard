import time
import socketio
import json
import datetime
from gps import *

#see https://gpsd.gitlab.io/gpsd/gpsd_json.html for more details on getting data from gpsd

delay = .5 #gps polling interval in seconds. Max polling rate 10hz for Adafruit Ultimate GPS (MTK3339 chipset)
    
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 

sio = socketio.Client()
sio.connect('http://localhost:3000')

def emitGpsData():
    while True:
        time.sleep(delay)
     
        try:
            report = gpsd.next()

            if report['class'] == 'TPV': #time-position-velocity report object
                data = {
                    'latitude': getattr(report,'lat',0.0),
                    'longitude': getattr(report,'lon',0.0),
                    'time': getattr(report,'time',''), #Time/date stamp in ISO8601 format, UTC. May have a fractional part of up to .001sec precision. May be absent if the mode is not 2D or 3D.
                    'altitude': getattr(report,'alt',0.0),#Altitude, height above ellipsoid, in meters. Probably WGS84.
                    'speed': getattr(report,'speed',0.0) * 2.2369, #mph converted from meters per second
                    'climb': getattr(report,'climb',0.0), #Climb (positive) or sink (negative) rate, meters per second.
                    'latitudeErr': getattr(report,'epy',0.0), #Latitude error estimate in meters. Certainty unknown.
                    'longitudeErr': getattr(report,'epx',0.0), #Longitude error estimate in meters. Certainty unknown.
                    'timeErr': getattr(report,'ept',0.0), #Estimated time stamp error in seconds. Certainty unknown.
                    'altitudeErr': getattr(report,'epv',0.0), #Estimated vertical error in meters. Certainty unknown.
                    'speedErr': getattr(report,'eps',0.0),#Estimated speed error in meters per second. Certainty unknown.
                    'climbErr': getattr(report,'epc',0.0) #Estimated climb error in meters per second. Certainty unknown.
                }
                    
                #print(data)
                sio.emit('gpsBaseData', json.dumps(data))
                
        except Exception:
            print("Unable to read from gps sensor, retrying...")
            now = datetime.datetime.now()
			timestamp = "%d-%d-%d_%d_%d_%d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
            
            error = {
                'description': 'GPS read error',
                'timeStamp': timestamp
            }
            sio.emit('error', error)
            continue


@sio.event
def connect():
    print("Gps connected to node server!")
    emitGpsData()
   
