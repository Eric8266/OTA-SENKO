import senko
import machine
from machine import Pin
from machine import ADC
import time
from time import sleep
import dht
import network
from CONFIG import SSID, PASSWORD, USER, REPOSITORY

#OTA = senko.Senko(
#  user="Eric8266", # Required
#  repo="OTA-SENKO", # Required
#  branch="master", # Optional: Defaults to "master"
#  working_dir="app", # Optional: Defaults to "app"
#  files = ["boot.py", "main.py"]
#)

#GITHUB_URL = "https://github.com/Eric8266/OTA-SENKO/"
#OTA = senko.Senko(url=GITHUB_URL, files=["boot.py", "main.py"])

OTA = senko.Senko(
  user=USER, repo=REPOSITORY, files = ["boot.py", "main.py"]
)

power_status = Pin(13, Pin.OUT)
wifi_status = Pin(12, Pin.OUT)
pump = Pin(14, Pin.OUT)
pump_status = Pin(16, Pin.IN)

power_status.on()  # Power is ON
wifi_status.off()  # Wifi is OFF
pump.off()  # Pump set to OFF
pump_status = pump

start = 1   # Start and keep running

def wifi_setup():  #Exit of Routine: wifi_status() = 1 means connected, 0 mean not connected
    wifi_status.off()  #Wifi LED is put OFF
    print('Trying to connect to Wifi . . . . . ')

    station = network.WLAN(network.STA_IF)

    station.active(True)
    
    station.connect(SSID, PASSWORD)
    start_time = time.time()

    stop_time = time.time()
    duration = stop_time - start_time
    while duration < 18:  #Must be connected within ~20 sec
        stop_time = time.time()
        duration = stop_time - start_time
              
        if duration > 15:
            print('Not connected, 15 sec time-out passed')
            wifi_status.off()  #Wifi LED is put OFF
            break
        if station.isconnected() == True:
            wifi_status.on()  #Wifi LED is put ON
            print('Wifi connection successfully to:',SSID,' with IP, Mask, Gateway, DNS:')
            print(station.ifconfig())
            break
    return(wifi_status)

########################################################################################
###                          MAIN PROGRAM STARTS HERE                                ###
########################################################################################

# Setup Wifi 1st time after fresh start
wifi_setup()
# Wifi ON: Status=1 or OFF: Status=0
# Blue LED is ON when connected

if wifi_status() == 1:
    print('Wifi Status = ON')
else:
    print('Wifi Status = OFF')
    
#################################################################################
########  When Wifi is ON, check for update via OTA on Github repository
########  UID = 'Eric8266'
########  Repo = 'OTA'
#################################################################################
    
if wifi_status() == 1:
    print('Check for Update')
    input('Wait here')
######################
###  NEW CODE OTA  ###

if OTA.update():
    print("Updated to the latest version! Rebooting...")
    machine.reset()
    

if OTA.fetch():
    print("A newer version is available!")
else:
    print("Up to date!")
    
