import os
import time
from pijuice import PiJuice # Import pijuice module
from subprocess import call

NO_AC = "NOT_PRESENT"


def shutdownPi():
	pijuice.rtcAlarm.SetWakeupEnabled(True)
	pijuice.power.SetWakeUpOnCharge(0)
	os.system("sudo shutdown -h now")
    
def checkPower():
    power_status = pijuice.status.GetStatus()['data']['powerInput']
    
    if(power_status == NO_AC):
        os.system("pkill -o chromium") #gracefully exit chrome to allow proper startup on next start instead of showing error + new tab page
        #shutdownPi() #commented out because I am handling shutdown using my pi dashcam app

while True:
    checkPower()
    time.sleep(2)
