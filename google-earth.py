# google-earth.py
# tangible interface

import sys
import serial
import time
import win32com.client

# Set location 1: UWO main gate
def goToUWO():
    lat = 43.009114
    lon = -81.261300
    alt = 100000
    tilt = 30
    azi = 0
    speed = 0.2
    range = 0
    altMode = 1
    ge.SetCameraParams(lat,lon,alt,altMode,range,tilt,azi,speed)
    print "Moving viewpoint to UWO main gate"

# Set location 2: Uluru (Ayers Rock)
def goToUluru():
    lat = -25.345
    lon = 131.036111
    alt = 100000
    tilt = 30
    azi = 180
    speed = 0.2
    range = 0
    altMode = 1
    ge.SetCameraParams(lat,lon,alt,altMode,range,tilt,azi,speed)
    print "Moving viewpoint to Uluru"

# initialize serial port
ser = serial.Serial('COM6', 9600, timeout=1)

# initialize Google Earth
ge =  win32com.client.Dispatch("GoogleEarth.ApplicationGE")
while not ge.IsInitialized():
    time.sleep(0.5)
    print "Waiting for Google Earth to initialize..."

# main loop
line = '0'
currentState = '0'
arduinoState = '0'
while 1:
    line = ser.readline()
    if len(line) > 0: arduinoState = line[0]
    if arduinoState != currentState:
        if arduinoState == '2':
            goToUWO()
            currentState = '2'
        if arduinoState == '3':
            goToUluru()
            currentState = '3'
        time.sleep(3)    
    sys.stdout.flush()