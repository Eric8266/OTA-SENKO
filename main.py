import dht
import machine
from machine import I2C, Pin
from machine import ADC
from machine import Timer
import time
from time import sleep
import network
from CONFIG import SSID, PASSWORD, USER, GITHUB_URL, GITHUB_RAW_URL, REPOSITORY, BRANCH, FILES, REMOTE_UPDATE, REMOTE_ACCESS, UPDATE_TIMER
from CONFIG import UPDATE_PERIODIC, UPDATE_PERIOD_MULT
import senko

##########################################################################################################
##  Assignments
##########################################################################################################
dht_pin = dht.DHT22(Pin(4)) # Uncomment it if you are using DHT22 and uncomment the next line
#dht_pin = dht.DHT11(Pin(4)) # Uncomment it if you are using DHT11 and comment the above line
power_status = Pin(13, Pin.OUT)
wifi_status = Pin(12, Pin.OUT)
pump = Pin(14, Pin.OUT)
pump_status = Pin(16, Pin.IN)
pgm_run_status = Pin(5, Pin.OUT)

##########################################################################################################
##  Variables setup
##########################################################################################################
power_status.on()  # Power is ON
wifi_status.off()  # Wifi is OFF
pump.off()  # Pump set to OFF
pump_status = pump
pgm_run_status.off()  # Pgm run status os OFF

start = 1   # Start and keep running
count = 0   # Reset the Delay Counter for Upgrade Checking. Total = count * UPDATE_PERIODIC mS.
            # E.g. daily check is 24 hrs means count must be 8640, if UPDATE_PERIODIC = 10000 mS
#update_check = 0  # Counts number of loops of count

url = GITHUB_RAW_URL
user = USER
repo = REPOSITORY
branch = BRANCH
files = FILES
        
##########################################################################################################
##  SubRoutines
##########################################################################################################

def mycallback(t):   # Routine to execute Timed Interrupt Service, e.g. once a day check for SW upgrade
    global count #, update_check
    count = count + 1
    pgm_run_status.on()
    print('8 minutes passed, continue program, iteration:',count)
#    if count == 8640:  # Is 24hrs event = 8640 * 10000 mSec
    if count == UPDATE_PERIOD_MULT:  # Blocks of 8 minutes
#        update_check = update_check + 1
#        stop_clock = time.perf_counter()
#        tijd = stop_clock-start_clock
#        print('Done. It took',round(tijd,2),'seconds !')
        print('')
#        print('Daily count reached, check for updates, reset NodeMCU if available updates applied. Update_check count =', UPDATE_PERIODIC_MULTIPLES)
        wifi_OTA()
        count = 0
    pgm_run_status.off()
    pass

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

def wifi_OTA():  #Checks if Wifi is ON, Check for Updates, if REMOTE_UPDATE = YES in CONFIG.py file
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
        #        else:    
        #            print('NO updates available, keep as is !!!')

    else:
        print('Wifi is OFF, continue without Wifi.')
        #######################################################################################################
        ########  Start rest of program, when Wifi was ON, check for update via OTA on Github repository done
        #######################################################################################################
#        print('Execute rest of the program')
    return

def read_dht():   #From DHT-11 temp/humidity module
    global temp, hum
##    dht_pin = dht.DHT22(Pin(4)) # Uncomment it if you are using DHT22 and uncomment the next line
 #   dht_pin = dht.DHT11(Pin(4)) # Uncomment it if you are using DHT11 and comment the above line
#    time.sleep(0.1)   # Delay 0.1 sec between assignment and measurement
    dht_pin.measure()
    temp = dht_pin.temperature()
    hum = dht_pin.humidity()
#        print('temp',temp,'hum',hum)
#        if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
#            msg = (b'{0:3.1f},{1:3.1f}'.format(temp, hum))
#            hum = round(hum, 2)
    # print('Temperature: {:3.2f}'.format(result.temperature/1.0))  # DHT22
    # print('Humidity: {:3.2f}'.format(result.humidity/1.0))  # DHT22
    return(temp, hum)

def read_moist():  #From FC-28 moisture sensor module
    global moi
    moi = 0
    moisture = ADC(0)
#    sleep(1.25)
    moi = moisture.read()
    moi = round((100*((1024 - moi)/556)))  #Moisture in %, Must be calibrated !!!
    return(moi) 


########################################################################################
###                          MAIN PROGRAM STARTS HERE                                ###
########################################################################################
###           Check if new Files are available, if YES, upload in NodeMCU            ###
########################################################################################

#if __name__ == '__main__':
try:
    # Allowes Exceptions, e.g. CTRL+C to interupt the program, and clear the HW timer
    while True:
        OTA = senko.Senko(
          url = GITHUB_RAW_URL,
          user = USER, # Required
          repo = REPOSITORY, # Required
          branch = BRANCH, # Optional: Defaults to "master"
        #  working_dir="app", # Optional: Defaults to "app"
          files = FILES  #["test1.py", "test2.py"]
        )

        #############################################################################################################
        if UPDATE_TIMER == "YES":   # If YES, Timer indicates when to check for updates on Github, periodic check
          # Instructions to initialise the Timer Interrupt Service Routine:
            tim = Timer(-1) # '-1' = Select a Virtual Timmer on the NodeMCU. NodeMCU has 2 timers, but 1 is for WiFi used.
          # Initialise Periodic shot firing after 10000mS = 10 Sec, and execute the 'mycallback' routine instructions
            tim.init(mode=Timer.PERIODIC, period=UPDATE_PERIODIC, callback=mycallback)
          #    tim.deinit()  # Deinitialises the timer. Stops the timer, and disables the timer peripheral.  
#            start_clock = time.perf_counter()
        #############################################################################################################
#        input('Stap1')
# Setup Wifi 1st time after fresh start
        wifi_setup()
        # Wifi ON: Status=1 or OFF: Status=0
        # Blue LED is ON when connected
            
        ######################################################################################
        ########  When Wifi is ON, check for update via OTA on Github repository
        ########  CONFIG.py contains the configuration parameters, e.g. REPOSITORY on Github
        ######################################################################################
#        input('Stap2')
        wifi_OTA()  # Check when Wifi=ON, than Update files if updates available on Github

        #######################################################################################################
        ########  When Wifi is ON, check for REMOTE_ACCESS with WebREPL
        #######################################################################################################
        if wifi_status() == 1:
            if REMOTE_ACCESS == "YES":
                print('Wifi is ON and REMOTE_ACCESS = YES in CONFIG.py, remote access with WebREPL is possible')
                import webrepl
                webrepl.start()

###  TEST Program, blinking LED, reading Temp & Hum

        Teller = 0
        while start == 1:
            Teller = Teller +1
            pump.on()
            sleep(0.5)
            pump.off()
            sleep(0.5)
            if Teller == 3600:  #3600 = ~1 uur
                read_dht()
                print('Teller:',Teller,'Temperature:',temp,'C, Humidity:',hum,'%')
                Teller = 0

        ###########################################################
        #  Continue Main Program
        ###########################################################

except KeyboardInterrupt:
    print("\nUser interrupted the program: CTRL+C. Performing Timer clearing.")
    tim.deinit()
    print("Exiting gracefully the program.")

except OSError:
    print('Failed to read DHT sensor.')
    tim.deinit()
    print("Exiting the program.")

