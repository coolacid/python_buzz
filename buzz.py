#!/usr/bin/env python
# PS2 Buzz! Controller library
import os
import usb.core
import usb.util

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
	print cfg
	intf = cfg[(0,0)]

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
	self.device.ctrl_transfer(0x0, 9, 0,0,[0x0,self.lights[0],self.lights[1],self.lights[2],self.lights[3]])

    def readcontroller(self):
	print "Reading controllers"

    def readlights(self):
	print (self.controller.leds(verbose=True))
	

if __name__=='__main__':
    buzz = buzz()
    buzz.setlights(0)
