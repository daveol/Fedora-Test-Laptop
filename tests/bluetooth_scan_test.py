#!/usr/bin/env python
import os
from avocado import Test
import bluetooth

'''
This test will scan for available bluetooth devices. If devices are found,
the test will succeed. The results of a successfully test are in the log.
If this test fails, it will abort  and raise an exception.
'''

class BluetoothScanTest(Test):
  def test():
      results = bluetooth.discover_devices(lookup_names = True)

      if (results ==None):
          self.fail("Bluetooth Scan test failed")

      self.log.debug("Bluetooth ping test succeeded: " + results)
