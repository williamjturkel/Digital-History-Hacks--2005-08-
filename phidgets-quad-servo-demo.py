# phidgets-quad-servo-demo.py
#
# wjt
# 18 mar 2007
#
# http://digitalhistoryhacks.blogspot.com
#
# Use Python to control Phidgets with 
# ctypes interface

from ctypes import *
import sys
import time

class pyPhidget:
    def __init__(self):
        if sys.platform == 'win32':
            self.dll = windll.LoadLibrary("C:\WINDOWS\system32\phidget21.dll")
        else:
            print "Platform not supported"
            
class pyPhidgetQuadServo(pyPhidget):
    
    def __init__(self,serial):
        pyPhidget.__init__(self)
        self.handle = c_long()
   
        self.dll.CPhidgetServo_create(byref(self.handle))
        result = self.dll.CPhidget_open(self.handle,c_int(serial))
        if result:
            print "No such phidget found, serial: %d" %(serial)
            return result
        self.dll.CPhidget_waitForAttachment(self.handle, c_int(0))

        devname = c_char_p()
        devserial = c_int()
        self.dll.CPhidget_getDeviceName(self.handle, byref(devname))
        self.dll.CPhidget_getSerialNumber(self.handle, byref(devserial))
        print "Device attached: %s, serial number: %d" % (devname.value, devserial.value)
        
    def close(self):
        self.dll.CPhidget_close(self.handle)
        self.dll.CPhidget_delete(self.handle)
        print "Device closed"

    def getMotorPosition(self, devindex):
        devpos = c_double()
        self.dll.CPhidgetServo_getMotorPosition(self.handle, c_int(devindex), byref(devpos))
        return devpos.value
    
    def setMotorPosition(self, devindex, devpos):
        self.dll.CPhidgetServo_setMotorPosition(self.handle, c_int(devindex), c_double(devpos))

    def convertValueToPulse(self, devvalue):
        return ((devvalue * 10.6) + 243.8)

    def convertPulseToValue(self, devpulse):
        return ((devpulse - 243.8) / 10.6)

# intialize
testphidget = pyPhidgetQuadServo(11454)

testphidget.setMotorPosition(0, 20)
time.sleep(2)

# test servo
for angle in range(20, 220, 10):
    testphidget.setMotorPosition(0, angle)
    time.sleep(0.2)
    print "Servo position 0. Angle: %d, Measured: %f" % (angle, testphidget.getMotorPosition(0))
for angle in range(220, 20, -10):
    testphidget.setMotorPosition(0, angle)
    time.sleep(0.2)
    print "Servo position 0. Angle: %d, Measured: %f" % (angle, testphidget.getMotorPosition(0))
    
# clean up
testphidget.close()