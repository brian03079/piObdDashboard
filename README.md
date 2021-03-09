# piObdDashboard
WIP raspberry-pi server-client app that pulls and displays data from a car's OBD2 port. Currently is able to display speed, rpm, and throttle %. More functionality and stability will be added as I continue working on it.

Helpful links:
https://github.com/autopi-io/py-obd
https://dash.plotly.com/
https://socket.io/get-started/chat

Required hardware:
1. OBD usb cable
    -bluetooth ones should work, though I used a usb cable for increased security, reliability, and not having to worry about battery drain
    -I used an OBDLink EX FORScan OBD Adapter. Others may also work.
3. Raspberry pi running raspbian (I used a pi 4)
4. SD card
5. External display
6. HDMI cable
7. micro usb power cable for the pi
8. Way to power the pi (ie. power bank, cigarette to usb car plug adapter)

Dependencies:
1. nodejs
2. npm
3. plotly (for js and python)
4. dash (python)
5. socketio (for js and python)
6. python3
7. express@4
8. python-OBD

How to run:
1. Make sure your car is on with the engine running
2. Make sure the OBD2 cable is plugged into the pi
3. Launch the server app using the command:
    node index.js
4. Launch the client app using the command:
    python3 obdDash.py
5. At this point the light on the OBD adapter should be blinking green, signifying that communication is happening between the car, obd adapter, and pi.
5. Open a web browser and navigate to localhost:3000
6. You should begin to see data populating

Notes:
1. This is WIP, so there will be lots of bugs :). For example there needs to be error handling and reconnection logic.
2. Did I mention bugs :)))? 
3. The graph gets updated every 1 second and there is no lag. Increasing this rate may cause the page to "fall behind" or lag when trying to update data, making it innaccurate. Perhaps it is asking too much from a raspberry pi. I am trying to find exactly at what point this starts happening, as well as finding ways to optimize. You can test if there is lag by shutting off the car. If there is no lag then the plotting of data should stop immediately.
