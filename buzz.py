#!/usr/bin/env python
# PS2 Buzz! Controller library
import usb.core
import usb.util
import traceback, sys, os
import time

class buzz:
    def __init__ (self):
	# ID 054c:1000 Sony Corp. Wireless Buzz! Receiver
	self.device = usb.core.find(idVendor=0x054c, idProduct=0x1000)
	self.interface = 0
	self.lights = [0,0,0,0]
	if self.device is None:
	    raise ValueError('Device not found')

	if self.device.is_kernel_driver_active(self.interface) is True:
	    self.kerneldriver = True
	    self.device.detach_kernel_driver(self.interface)
	else:
	    self.kerneldriver = False

	self.device.set_configuration()
	usb.util.claim_interface(self.device, self.interface)
	cfg = self.device.get_active_configuration()
	self.endpoint = cfg[(0,0)][0]

    # TODO: Should figure out how to re-attach the kernel driver
    # But this doesn't seem to work
#    def __del__(self):
	#print "release claimed interface"
	#usb.util.release_interface(self.device, self.interface)
	#if self.kerneldriver == True:
	#    print "now attaching the kernel driver again"
	#    dev.attach_kernel_driver(self.interface)

    def setlights(self, control):
	print "setting lights"
	self.lights[0] = 0xFF if control & 1 else 0x00
	self.lights[1] = 0xFF if control & 2 else 0x00
	self.lights[2] = 0xFF if control & 4 else 0x00
	self.lights[3] = 0xFF if control & 8 else 0x00
	self.device.ctrl_transfer(0x21, 0x09, 0x0200,0,[0x0,self.lights[0],self.lights[1],self.lights[2],self.lights[3],0x0,0x0])

    def readcontroller(self):
	try: 
	    cfg = self.device.get_active_configuration()
	    self.endpoint = cfg[(0,0)][0]
	    data = self.device.read(self.endpoint.bEndpointAddress, self.endpoint.wMaxPacketSize)
	except usb.core.USBError as e: 
	    if e[0] != 110:
		traceback.print_exc(file=sys.stdout)
	    data = None
	return data

    def readlights(self):
	
	print (self.controller.leds(verbose=True))
	

if __name__=='__main__':
    buzz = buzz()
    for x in range(16):
	buzz.setlights(x)
	time.sleep(1)
    buzz.setlights(0)
    while True:
	r = buzz.readcontroller()
	if r != None:
	    print r
