#!/usr/bin/env python
import os
import subprocess as subp
from subprocess import *
from avocado import Test

class WifiScanAP(Test):
  def test():

      targetDeviceMac = '8C:1A:BF:0D:31:A9'
      bluetoothChannel = '2'
      port = 1


      print("Bluetooth ping test: testing " + targetDeviceMac)
      p = subp.Popen(['sudo', 'l2ping', '8C:1A:BF:0D:31:A9','-c', '5'], stdout=subp.PIPE, stderr=subp.PIPE)

      stdout, stderr = p.communicate()
      res = stdout.rstrip()

      if "5 sent, 5 received" in res:
         self.log.debug("Bluetooth ping test succeeded: + res")
      else:
          self.fail("Bluetooth ping test: pinging " + targetDeviceMac + " failed")


