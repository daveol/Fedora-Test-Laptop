#!/usr/bin/env python
import os
from avocado import Test
import bluetooth
from utils import utils

'''
This test will scan for available bluetooth devices and checks if the
bluetooth device that is specified in the YAML file is available.
'''

class BluetoothScan(Test):
    def test(self):
        testdata = utils.load_yaml(self, "data/bluetooth_data.yaml")
        self.targetDeviceMac = testdata['testdata']['addr']
        
        results = bluetooth.discover_devices(lookup_names = True)
        detected = False
        
        for res in results:
            if res[0] == self.targetDeviceMac:
                detected = True
                
        if not detected:
            self.fail("Bluetooth Scan test failed")
            
#        self.log.debug("Bluetooth Scan test succeeded: " + results)
