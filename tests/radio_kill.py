#!/usr/bin/env python

import subprocess as subp
import time
from avocado import Test
from utils import internet, utils

class RadioKill(Test):
    def test(self):
        wifidata = utils.load_yaml(self, "data/internet_data.yaml")
        accessPoint = wifidata['access_point_1']['ssid']
        accessPointPass = wifidata['access_point_1']['pass']
        self.interface = wifidata['wireless_interface']

        bluetoothdata = utils.load_yaml(self, "data/bluetooth_data.yaml")
        self.targetDeviceMac = bluetoothdata['testdata']['addr']

        self.block_and_verify(accessPoint, accessPointPass)
        self.unblock_and_verify(accessPoint, accessPointPass)
        
    def block_and_verify(self, ssid, password):
        p = subp.call(['rfkill', 'block', 'all'])     

        connected = internet.connect(ssid, password)

        if(connected == True):
            self.fail("Wi-Fi still works despite radio kill on network {0}".format(ssid))
        
        p = subp.Popen(['l2ping', self.targetDeviceMac ,'-c', '5'], stderr= subp.STDOUT, stdout = subp.PIPE)
        result = p.communicate()[0]
        bluetootResult = p.returncode

        if(bluetootResult == 0):
            self.fail("Bluetooth still works despite radio kill on device {0}".format(self.targetDeviceMac))

    def unblock_and_verify(self, ssid, password):
        p = subp.call(['rfkill', 'unblock', 'all'])     

        time.sleep(5);

        internet.connect(ssid, password)
        gateway = internet.get_gateway(self.interface, self)
        pingResult = internet.pingtest_hard(gateway, self.interface, self)

        self.log.debug("Internet is working on network {0}".format(ssid))
            
        p = subp.Popen(['sudo', 'l2ping', self.targetDeviceMac ,'-c', '1'], stderr= subp.STDOUT, stdout = subp.PIPE)
        result = p.communicate()[0]
        bluetoothResult = p.returncode

        if(bluetoothResult != 0):
            self.fail("Bluetooth does not work on device {0}".format(self.targetDeviceMac))
        self.log.debug("Bluetooth is working on device {0}".format(self.targetDeviceMac))


    
