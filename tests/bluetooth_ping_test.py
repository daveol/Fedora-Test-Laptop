#!/usr/bin/env python
import os
import subprocess as subp
from avocado import Test
import bluetooth
from utils import utils

'''
This test will ping a specific device. The device needs to be specified in the
YAML file. If the device responds, the result will be found in the debug log.
If the test fails, a fail exception will be raised.
'''
class BluetoothPingTest(Test):
    def test(self):
      testdata = utils.load_yaml(self, "data/bluetooth_data.yaml")
      self.targetDeviceMac = testdata['testdata']['addr']

      p = subp.Popen(['sudo', 'l2ping', self.targetDeviceMac ,'-c', '5'], stdout=subp.PIPE, stderr=subp.PIPE)
      result = p.communicate()[0]
      returnCode = p.returncode

      if returnCode != 0 :
          self.fail("Could not ping " + self.targetDeviceMac)

     self.log.debug("Ping test working {0}".format(result))
