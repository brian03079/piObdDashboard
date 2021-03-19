WIP raspberry-pi dashboard app that pulls and displays data from a car's OBD2 port. Currently is able to display speed, rpm, throttle %, cabin temp and humidity. More functionality and stability will be added as I continue working on it. 

Additional planned changes:
1. Tabs for navigating addtional + different sensor data
2. Saving logged data

Possible planned features:
1. IMU sensor integration to show data such as orientation, position, velocity, acceleration

Helpful links:
https://github.com/autopi-io/py-obd
https://dash.plotly.com/
https://socket.io/get-started/chat

Required hardware:
1. OBD usb cable [Link](https://www.amazon.com/gp/product/B081VQVD3F/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1)
    -bluetooth ones should work, but I opted for a usb cable for better security, reliability, and not having to worry about battery drain
    -I used an OBDLink EX FORScan OBD Adapter. Others may also work.
3. Raspberry pi running raspberry pi os [Link](https://www.sparkfun.com/products/15447)
4. SD card
5. External display [Link](https://www.amazon.com/gp/product/B07S51QDTG/ref=ppx_yo_dt_b_asin_title_o06_s00?ie=UTF8&psc=1) (optional if you are using your phone to connect to the pi via phone hotspot sharing)
6. HDMI to micro HDMI cable or adapter (optional, see above)
7. Power cable for the pi
8. Way to power the pi (ie. power bank, cigarette to usb car plug adapter)

Optional hardware:
1. (Optional) DHT22/11 temp and humidity sensor [Link](https://www.amazon.com/gp/product/B073F472JL/ref=ppx_yo_dt_b_search_asin_image?ie=UTF8&psc=1)
2. PiJuice HAT uninterruptible power supply [Link](https://www.sparkfun.com/products/14803) - This will prevent hard shutdowns on the pi when the car is turned off. I am also tweaking start/shutdown scripts to automate everything. 

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
5. Open a web browser and navigate to the web app localhost:3000. This can be done on the pi itself, or your phone. You will almost certainly get much better performance using your phone and each method has its benefits. To use your phone, enable hotspot sharing and connect your pi to it. Next, find out the ip address given to your pi (ie. 192.168.1.20) and enter it into your browser followed by the port number like "192.168.1.20:3000").
6. Data should start populating. The axes on the graphs auto resize based on the speed, rpm, and time. Each graph also has adjustment options if you hover over the top right of each.

Notes:
1. This is WIP, so there will be lots of bugs :). For example there needs to be error handling and reconnection logic.
2. Did I mention bugs :)))? 
3. Code will be cleaned and refactored as more work is being done
4. I have set the polling rate of the web app to .3 seconds. If you are using the pi to display the dashboard, this is the fastest speed it can draw without lagging. If you are not displaying with the pi and instead use your phone, you can increase the rate to .15s or more depending on specs. Most cpu cycles are taken up by plotting the two graphs.
5. This dashboard app can also be used in conjunction with the raspberry pi dashcam I made in my other repository: https://github.com/brian03079/piDashcam . The pi 4 seems to handle running both at the same time fine.
6. You can adjust most of the code without having to be at your car by running the mockObdGenerator.py in place of the piObd.py. This will run a simulation instead.
