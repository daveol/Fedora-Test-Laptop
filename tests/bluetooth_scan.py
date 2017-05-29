#!/usr/bin/env python
import os
from avocado import Test
import bluetooth
from utils import utils
import re



class BluetoothScan(Test):
    '''
    This test requires the pybluez package
    This test will scan for available bluetooth devices and checks if the
    bluetooth device that is specified in the YAML file is available.
    '''
    def setUp(self):
        testdata = utils.load_yaml(self, "data/bluetooth_data.yaml")
        try:
            self.targetDeviceMac = self.testdata['testdata']['addr']
        except:
            self.skip('Invalid testdata')

        if not bool(re.match('^' + '[\:\-]'.join(['([0-9a-f]{2})']*6) + '$', self.targetDeviceMac.lower())):
            self.skip('Target Device mac address invalid')

    def test(self):
        results = bluetooth.discover_devices(lookup_names = True)
        detected = False
        
        for res in results:
            if res[0] == self.targetDeviceMac:
                detected = True
                
        if not detected:
            self.fail("Target device not found")
            
#        self.log.debug("Bluetooth Scan test succeeded: " + results)
