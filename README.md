WIP raspberry-pi dashboard app that pulls and displays data from a car's OBD2 port. Currently is able to display speed, rpm, throttle %, cabin temp and humidity. More functionality and stability will be added as I continue working on it.

Helpful links:
https://github.com/autopi-io/py-obd
https://dash.plotly.com/
https://socket.io/get-started/chat

Required hardware:
1. OBD usb cable
    -bluetooth ones should work, but I opted for a usb cable for better security, reliability, and not having to worry about battery drain
    -I used an OBDLink EX FORScan OBD Adapter. Others may also work.
3. Raspberry pi running raspberry pi os (I used a pi 4 with 4gb ram)
4. SD card
5. External display
6. HDMI cable
7. Power cable for the pi
8. Way to power the pi (ie. power bank, cigarette to usb car plug adapter)

Optional hardware:
1. (Optional) DHT22/11 temp and humidity sensor
2. PiJuice HAT uninterruptible power supply (ups) - This will prevent hard shutdowns on the pi when the car is turned off. I am also tweaking start/shutdown scripts to automate everything. 

Dependencies:
1. nodejs
2. npm
3. plotly js
4. python-OBD
5. socketio (js and python3)
6. python3
7. express >= 4
8. adafruit_dht (if you are using the DHT22/11 sensors)

How to run:
1. Make sure your car is on with the engine running
2. Make sure the OBD2 cable is plugged into the pi and car
3. Launch the server app using the command:
    node index.js
4. Launch the python OBD logger app using the command:
    python3 obdDash.py
5. (Optional) If you have a DHT22/11 sensor hooked up to the pi, launch the python temperature/humidity logger app:
    python3 tempMonitor.py
5. After launching obdDash.py, you should see "Connected to node server!" and the light on the OBD adapter should be blinking green, signifying that communication is happening between the car, obd adapter, and pi.
5. Open a web browser and navigate to the web app localhost:3000
6. Data should start populating. The axes on the graphs auto resize based on the speed, rpm, and time. Each graph also has adjustment options if you hover over the top right of each.

Notes:
1. This is WIP, so there will be lots of bugs :). For example there needs to be error handling and reconnection logic.
2. Did I mention bugs :)))? 
3. Code will be cleaned and refactored as more work is being done
4. I have set the polling rate of the web app to .3 seconds. Any faster and the pi will begin to lag and the data will no longer be realtime. Most of the cpu cycles are taken up by plotting the two graphs.
5. This dashboard app can also be used in conjunction with the raspberry pi dashcam I made in my other repository: https://github.com/brian03079/piDashcam . The pi 4 seems to handle running both at the same time fine.
6. You can adjust most of the code without having to be at your car by running the mockObdGenerator.py in place of the piObd.py. This will run a simulation instead.
