# phidgets-interface-kit-demo.py
#
# wjt
# 16, 25 mar 2007
# 23 apr 2007
#
# http://digitalhistoryhacks.blogspot.com
#
# Use Python to control Phidgets with 
# ctypes interface
#
# This version has support for callbacks

# from ctypes import *
# import sys

# class pyPhidget:
#    def __init__(self):
#        if sys.platform == 'win32':
#            self.dll = windll.LoadLibrary("C:\WINDOWS\system32\phidget21.dll")
#        else:
#            print "Platform not supported"
            
# class pyPhidgetInterfaceKit(pyPhidget):

#    def __init__(self,serial):
        # pyPhidget.__init__(self)
        # self.handle = c_long()
       
        # self.dll.CPhidgetInterfaceKit_create(byref(self.handle))
        # CPhidgetHandle, Int
        # result = self.dll.CPhidget_open(self.handle,c_int(serial))
        # if result:
        #    print "No such phidget found, serial: %d" %(serial)
        #   return result
        # CPhidgetHandle, long (0 is infinite)
        # self.dll.CPhidget_waitForAttachment(self.handle, c_int(0))

        # CPhidgetHandle, char **
        # devname = c_char_p()
        # self.dll.CPhidget_getDeviceName(self.handle, byref(devname))
        # CPhidgetHandle, int *
        # devserial = c_int()
        # self.dll.CPhidget_getSerialNumber(self.handle, byref(devserial))
        # print "Device attached: %s, serial number: %d" % (devname.value, devserial.value)
        
    # def close(self):
        # CPhidgetHandle
        # self.dll.CPhidget_close(self.handle)
        # CPhidgetHandle
        # self.dll.CPhidget_delete(self.handle)
        # print "Device closed"

    def getNumInputs(self):
        devnuminputs = c_int()
        self.dll.CPhidgetInterfaceKit_getNumInputs(self.handle, byref(devnuminputs))
        return devnuminputs.value

    def getInputState(self, devindex):
        devinstate = c_int()
        self.dll.CPhidgetInterfaceKit_getInputState(self.handle, c_int(devindex), byref(devinstate))
        return bool(devinstate.value)

    def getNumOutputs(self):
        devnumoutputs = c_int()
        self.dll.CPhidgetInterfaceKit_getNumOutputs(self.handle, byref(devnumoutputs))
        return devnumoutputs.value
    
    def getOutputState(self, devindex):
        devoutstate = c_int()
        self.dll.CPhidgetInterfaceKit_getOutputState(self.handle, c_int(devindex), byref(devoutstate))
        return bool(devoutstate.value)

    def setOutputState(self, devindex, devnewstate):
        self.dll.CPhidgetInterfaceKit_setOutputState(self.handle, c_int(devindex), c_int(devnewstate))

    def getNumSensors(self):
        devnumsensors = c_int()
        self.dll.CPhidgetInterfaceKit_getNumSensors(self.handle, byref(devnumsensors))
        return devnumsensors.value

    def getRatiometric(self):
        devratiometric = c_int()
        self.dll.CPhidgetInterfaceKit_getRatiometric(self.handle, byref(devratiometric))
        return devratiometric.value

    def setRatiometric(self, devnewval):
        self.dll.CPhidgetInterfaceKit_setRatiometric(self.handle, c_int(devnewval))

    def getSensorValue(self, devindex):
        devsensorval = c_int()
        self.dll.CPhidgetInterfaceKit_getSensorValue(self.handle, c_int(devindex), byref(devsensorval))
        return devsensorval.value

    def getSensorRawValue(self, devindex):
        devsensorrawval = c_int()
        self.dll.CPhidgetInterfaceKit_getSensorRawValue(self.handle, c_int(devindex), byref(devsensorrawval))
        return devsensorrawval.value

    def getSensorChangeTrigger(self, devindex):
        devsensorchgtrig = c_int()
        self.dll.CPhidgetInterfaceKit_getSensorChangeTrigger(self.handle, c_int(devindex), byref(devsensorchgtrig))
        return devsensorchgtrig.value

    def setSensorChangeTrigger(self, devindex, devnewval):
        self.dll.CPhidgetInterfaceKit_setSensorChangeTrigger(self.handle, c_int(devindex), c_int(devnewval))

    # def setOnSensorChangeHandler(self, devindex):

        # def py_handler(self, a, index, value):
            # print "In handler"
            # print "self ", str(self)
            # print "a ", str(a)
            # print "index ", str(index)
            # print "value ", str(value)

        # self.dll.CPhidgetInterfaceKit_set_OnSensorChange_Handler
        #   (self.handle, int (*fptr)(self.handle, void *, int, int), void *)
    
        # SensorChangeTrigger_Handler = CFUNCTYPE(c_int, c_long, c_void_p, c_int, c_int)

        # callback = SensorChangeTrigger_Handler(py_handler)

        # self.dll.CPhidgetInterfaceKit_set_OnSensorChange_Handler(self.handle, callback, None)

# intialize
# testphidget = pyPhidgetInterfaceKit(31183)

# test the various functions that return info about phidget
# print "Number of inputs: %d" % (testphidget.getNumInputs())
# print "Number of outputs: %d" % (testphidget.getNumOutputs())
# print "Number of sensors: %d" % (testphidget.getNumSensors())

# Turn on LED on Output 0
# testphidget.setOutputState(0,1)

# Testing nonratiometric Temperature sensor on Sensor 6
# testphidget.setRatiometric(0)

# Testing ratiometric Light sensor on Sensor 0
# testphidget.setRatiometric(2)

# Break out of loop by closing NO switch on Input 0
# while not(testphidget.getInputState(0)):
    # pass
    # print "Sensor 0: %s\t" % (testphidget.getSensorRawValue(0))
    # print "Sensor 6: %s\t" % (testphidget.getSensorRawValue(6))

# Test callbacks
    
# print "Sensor change trigger 0: %d" % (testphidget.getSensorChangeTrigger(0))
# print "Setting sensor change trigger 0 to 15"
# testphidget.setSensorChangeTrigger(0, 15)
# print "Sensor change trigger 0: %d" % (testphidget.getSensorChangeTrigger(0))
    
# testphidget.setOnSensorChangeHandler(0)
    
# Break out of loop by closing NO switch on Input 0
# while not(testphidget.getInputState(0)):
#    pass

# Turn off LED on Output 0
# testphidget.setOutputState(0,0)
    
# clean up
# testphidget.close()