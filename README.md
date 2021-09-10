# Raspberry Pi OBD Dashboard
## _Background_

Out of curiosity and for fun, I thought it would be neat to make a digital "dashboard" for my car using a raspberry pi. I originally wanted a way to read and graph information like speed and engine RPM but eventually expanded the features to include temperature, gps, air quality monitoring, etc.

## Overview
![Showing the data](https://github.com/brian03079/piObdDashboard/blob/develop/photos/monitors.png)
[Video demonstration](https://www.youtube.com/watch?v=rTwZY9AT3mg&ab_channel=BrianChan) (older version of the app but helps demonstrate the graphing)

##  Main Features 

- Info such as vehicle speed, RPM, idle, runtime, etc.
- Graphing of speed and RPM to track driving habits
- Cabin temperature + humidity monitoring
- Diagnostic Trouble Codes (DTC) statuses
- GPS monitor
- Air quality monitor
- Vehicle orientation + acceleration statuses

## Program structure

The dashboard is a combination of python3 apps which run in the background and send information to web pages that is then displayed to the user. There are two web pages:

 - A primary one that mainly shows telemetry data about the car itself such as speed, rpm, engine statistics
 - A misc web page that shows GPS, air quality, orientation/acceleration, and logging information

The pages are hosted using a node server running on the pi. When the pi is started, an entry in /home/pi/.config/lxsession/LXDE-pi/autostart :

> @bash /home/pi/piObdDashboard/startApps.sh

automatically executes a bash script which prepares and starts the background apps and browsers to begin showing data to the user. One of the apps that is started is called obdMisc.py which can optionally detect button presses which can restart and shutdown the pi.


## Hardware requirements
### Primary Page:
 - [Raspberry Pi 4](https://www.sparkfun.com/products/15447). A Pi 3 _might_ be fast enough, but I still recommend a Pi 4 because of the big performance upgrade. If you use a Pi 3 you may need to adjust the update intervals in the python3 apps.
 - [SD Card](https://www.amazon.com/gp/product/B07FCMKK5X/ref=ppx_yo_dt_b_search_asin_image?ie=UTF8&psc=1). Any decently fast one should be fine.
 - [LCD panel](https://www.amazon.com/gp/product/B07S51QDTG/ref=ppx_yo_dt_b_asin_title_o06_s00?ie=UTF8&psc=1) with minimum resolution of 1024x600 and small enough to be mounted in the car (optional if you are using your phone to connect to the pi via phone hotspot sharing).
 - [Windshield mount](https://www.amazon.com/gp/product/B08BJ9R7MS/ref=ppx_yo_dt_b_search_asin_image?ie=UTF8&psc=1) or a way to secure the display
 - [OBD usb cable](https://www.amazon.com/gp/product/B081VQVD3F/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1). This is how we will be getting the car's data. Bluetooth ones should work, but I opted for a usb cable for better security, reliability, and not having to worry about battery drain when the car is off.
 - [OBD extension cable](https://www.amazon.com/gp/product/B01C2M2ZZG/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1). This prevents your legs from bumping into the USB OBD adapter and allows you some more wiggle room for mounting the pi.
 - [DHT22 temp/humidity sensor](https://www.amazon.com/gp/product/B073F472JL/ref=ppx_yo_dt_b_search_asin_image?ie=UTF8&psc=1)
 - Power and video cables for the pi and display
 - Cigarette socket to usb adapter with recommended output of 15w. Optional if your car already has a usb port that meets these power requirements. Many ports will only supply 500 milliamps (2.5 watts) which is not nearly enough for the Pi 4.
 
### Misc Page:
 - [Adafruit PMSA003I Air Quality Breakout](https://www.adafruit.com/product/4632). Measures air quality.
 - [Adafruit Ultimate GPS HAT](https://www.adafruit.com/product/2324) - Retrieves GPS info.
 - [Adafruit 9-DOF Absolute Orientation IMU Fusion Breakout - BNO055](https://www.adafruit.com/product/2472) - Retrieves pitch, roll, etc. of car
 - [GPS Antenna](https://www.adafruit.com/product/960) - Needed for the gps or you won't get reception
 - [SMA to uFL/u.FL/IPX/IPEX RF Adapter Cable](https://www.adafruit.com/product/851) - Adapter cable to connect the GPS hat to the external antenna

Note that if you want to display both pages, you will need 2 screens. Its also possible to modify the pages to have a button to switch between the pages which i will probably implement at a later date.
### Optional (If you want to be able to easily shutdown the pi or restart the apps):
 - Jumper wires
 - Breadboard
 - Button switches

There are cleaner ways to implement this but it was the cheapest solution.
## Hardware Setup
Mount the Pi and Display in the car to your liking. The rest of this sections goes over how to connect the various sensors to the pi :))

### OBD functionality:
Attach the OBD extension cable to the car's OBD port. This varies depending on the car but is often around the driver's side footwell area. Next, plug the USB OBD adapter into the extension cable, and then into one of the Pi's usb ports

### Temperature/Humidity sensor:
TODO

### GPS 
TODO

### Orientation sensor:
TODO

## Pi Setup
This section automatically assumes that you have installed and booted into Raspberry Pi OS. Lets first make sure that everything is updated before installing any packages:
```
$ sudo apt update
$ sudo apt full-upgrade
```
Next, open up preferences and make sure under the interfaces tab that everything is set to 'Enabled' except for the serial console by going to:
> Preferences -> Raspberry Pi Configuration -> Interfaces-> Serial Console (set to off)

The serial console needs to be disabled or it will end up interfering with the gps software. However, if you arent using the GPS then this doesn't matter.

Disable Screen blanking so as the pi is displaying data the screen does not turn off:
> Preferences -> Raspberry Pi Configuration -> Display -> Screen Blanking (set to off)

## Software Installation
(if you dont have certain sensors, you can just skip that software)
### NVM, Node.js:
```
$ curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
$ nvm install stable
```
### Node.js dependencies:
```
$ npm install socket.io
$ npm install express
```
### OBD (for retrieving car data):
```
$ pip3 install obd
```
### Networking for the python apps:
```
$ pip3 install "python-socketio[client]"
```
### Orientation sensor:
```
$ pip3 install adafruit-circuitpython-bno055
```
### Air Sensor:
```
$ pip3 install adafruit-circuitpython-pm25
```
### Temperature Sensor:
```
$ pip3 install adafruit-circuitpython-dht
```
### GPS:
```
$ pip3 install gps
$ sudo apt install gpsd gpsd-clients python-gps
$ sudo systemctl stop gpsd.socket
$ sudo systemctl disable gpsd.socket
```
### 'Unclutter' app which removes the mouse cursor when idle:
```
$ sudo apt install unclutter
```

Finally, lets clone the dashboard repo:
```
$ git clone https://github.com/brian03079/piObdDashboard.git 
```
Once inside the repo, you can copy the autostart file to 
> /home/pi/.config/lxsession/LXDE-pi/autostart

Or if you already have an autostart file there, then simply append 
> @bash /home/pi/piObdDashboard/startApps.sh 

to the end of your existing autostart file. The '@' annotation simply tries to rerun the command if it fails the first time, but isn't required. Note that depending on what apps you want to start or omit, you may need to comment out some of the python files or lines in startApps.sh and restartApps.sh. 

## Running the Apps
At this point you should be able to test if things are working by manually running the '.sh' files. If you want to test running an individual program, run the node server followed by the name of the python program you want to run. Then open a browser and point it to whichever page that that program sends data to. 
TODO


## License

MIT
