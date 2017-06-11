#!/usr/bin/env python

import subprocess as subp
import time
from avocado import Test
from utils import internet, utils

class RadioKill(Test):
    """
    Gets the first access point from internet_data and the MAC address
    from the first bluetooth enabled device from bluetooth_data.
    Radio signals are blocked and the Wi-Fi and Bluetooth connections
    should fail.
    Radio signals are unblocked and the Wi-Fi and Bluetooth connections
    should work.

    """
    def setUp(self):
        wifidata = utils.load_yaml(self, "data/internet_data.yaml")
        bluetoothdata = utils.load_yaml(self, "data/bluetooth_data.yaml")

        if 'access_point_1' not in wifidata:
            self.skip("No AP found in the yaml config")

        if ('ssid' not in wifidata['access_point_1'] or
            'pass' not in wifidata['access_point_1']):
            self.skip("No AP data found in the yaml config")

	    if 'testdata' not in bluetoothdata:
            self.skip("No bluetooth data found in the yaml config")

        if 'addr' not in bluetoothdata['testdata']:
            self.skip("No bluetooth addr found in the yaml config")

        self.ap_ssid = wifidata['access_point_1']['ssid']
        self.ap_pass = wifidata['access_point_1']['pass']
        self.targetDeviceMac = bluetoothdata['testdata']['addr']

    def test(self):
        self.wireless_interface = internet.get_active_interface('wifi', self)
        self.block_and_verify()
        self.unblock_and_verify()

    def block_and_verify(self):
        p = subp.call(['rfkill', 'block', 'all'])

        connected = internet.connect(self.ap_ssid, self.ap_pass)

        if(connected == True):
            self.fail("Wi-Fi still works despite radio kill on network {0}".format(self.ap_ssid))

        p = subp.Popen(['l2ping', self.targetDeviceMac ,'-c', '5'], stderr= subp.STDOUT, stdout = subp.PIPE)
        bluetoothResult = p.returncode

        if bluetoothResult == 0:
            self.fail("Bluetooth still works despite radio kill on device {0}".format(self.targetDeviceMac))

    def unblock_and_verify(self):
        p = subp.call(['rfkill', 'unblock', 'all'])

        # wait for radio services to unblock
        time.sleep(5);

        internet.connect(self.ap_ssid, self.ap_pass)
        gateway = internet.get_gateway(self.wireless_interface, self)
        pingResult = internet.pingtest_hard(gateway, self.wireless_interface, self)

        self.log.debug("Internet is working on network {0}".format(self.ap_ssid))

        p = subp.Popen(['sudo', 'l2ping', self.targetDeviceMac ,'-c', '1'], stderr= subp.STDOUT, stdout = subp.PIPE)
        bluetoothResult = p.returncode

        if bluetoothResult != 0:
            self.fail("Bluetooth does not work on device {0}".format(self.targetDeviceMac))
        self.log.debug("Bluetooth is working on device {0}".format(self.targetDeviceMac))
