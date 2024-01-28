import machine
from machine import Pin
from machine import ADC
import time
from time import sleep
import dht
import network
from CONFIG import SSID, PASSWORD, USER, GITHUB_URL, GITHUB_RAW_URL, REPOSITORY, BRANCH, FILES, REMOTE_UPDATE
#print('Before import of senko')
import senko
#print('After import of senko')

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

def wifi_check():
    station = network.WLAN(network.STA_IF)
    print("Check if connected to Wifi")
    if station.isconnected() == True:
        print('Still connected to:',ssid)
        wifi_status.on()  #Wifi LED is put ON
    else:
        print('Reconnect to Wifi')
        wifi_setup()
        #wifi_status updated from wifi_setup() routine
        # Needs WORK HERE
        #IF wifi_status = 1 continue program with Blynk Connected
        #IF Wifi_status = 0 continue without Wifi and Blynk
    print('Test wifi_check status:',wifi_status())
    return(wifi_status)

def read_dht():   #From DHT-11 temp/humidity module
    global temp, hum
#    dht_pin = dht.DHT22(Pin(4))  # Comment it if you are using DHT22 and uncomment the next line
    dht_pin = dht.DHT11(Pin(4)) # Uncomment it if you are using DHT11 and comment the above line
    temp = hum = 0
    try:
        sleep(1.25) # Sample period is 1 sec
        dht_pin.measure()
        temp = dht_pin.temperature()
        hum = dht_pin.humidity()
        if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
            msg = (b'{0:3.1f},{1:3.1f}'.format(temp, hum))
            hum = round(hum, 2)
            return(msg, temp, hum)
        else:
            return('Invalid DHT sensor readings.')
    except OSError as e:
        return('Failed to read DHT sensor.')

def read_moist():  #From FC-28 moisture sensor module
    global moi
    moi = 0
    moisture = ADC(0)
    sleep(1.25)
    moi = moisture.read()
    moi = round((100*((1024 - moi)/556)))  #Moisture in %, Must be calibrated !!!
    return(moi) 


########################################################################################
###                          MAIN PROGRAM STARTS HERE                                ###
########################################################################################
###           Check if new Files are available, if YES, upload in NodeMCU            ###
########################################################################################
url = GITHUB_RAW_URL
user = USER
repo = REPOSITORY
branch = BRANCH
files = FILES

OTA = senko.Senko(
  url = GITHUB_RAW_URL,
  user = USER, # Required
  repo = REPOSITORY, # Required
  branch = BRANCH, # Optional: Defaults to "master"
#  working_dir="app", # Optional: Defaults to "app"
  files = FILES  #["test1.py", "test2.py"]
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

# Setup Wifi 1st time after fresh start
wifi_setup()

# Wifi ON: Status=1 or OFF: Status=0
# Blue LED is ON when connected
    
######################################################################################
########  When Wifi is ON, check for update via OTA on Github repository
########  CONFIG.py contains the configuration parameters, e.g. REPOSITORY on Github
######################################################################################
    
if wifi_status() == 1:
    print('Wifi is ON, Check for Updates, if REMOTE_UPDATE = YES in CONFIG.py file')

####################################################
###  ONLY check for new Versions, NO Updates     ###
####################################################
#     if OTA.fetch():
#         print("A newer version is available!")
#     else:
#         print("Up to date! Ready for the rest of the program")
    
###########################################################
###  Check for new Versions, Update and Reboot NodeMCU  ###
###########################################################
    if REMOTE_UPDATE == "YES":        
#        print('UPDATE')
        if OTA.update():
            print("Updated to the latest file versions ! Rebooting...")
            machine.reset()
        else:    
            print('NO updates available, keep as is !!!')

else:
    print('Wifi is OFF, continue without Wifi.')
#######################################################################################################
########  Start rest of program, when Wifi was ON, check for update via OTA on Github repository done
#######################################################################################################


