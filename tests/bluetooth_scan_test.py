#!/usr/bin/env python
import os
from avocado import Test
import bluetooth
from utils import utils

'''
This test will scan for available bluetooth devices and checks if the
bluetooth device that is specified in the YAML file is available.
'''

class BluetoothScanTest(Test):
  def test():
      testdata = utils.load_yaml(self, "data/bluetooth_data.yaml")
      self.targetDeviceMac = testdata['addr']

      results = bluetooth.discover_devices(lookup_names = True)

      if self.targetDeviceMac not in results:
          self.fail("Bluetooth Scan test failed")

      self.log.debug("Bluetooth Scan test succeeded: " + results)
