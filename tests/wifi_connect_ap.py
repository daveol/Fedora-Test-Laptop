#!/usr/bin/env python

from avocado import Test
from utils import internet, utils
import time
class WifiConnectAP(Test):
    """
    Uses the first access point from internet_data to ping the default
    gateway using internet utils.

    """
    def setUp(self):
        wifidata = utils.load_yaml(self, "data/internet_data.yaml")

        if 'wireless_interface' not in wifidata:
            self.skip("No wireless interface in the yaml config")

        if 'access_point_1' not in wifidata:
            self.skip("No AP found in the yaml config")

        if ('ssid' not in wifidata['access_point_1'] or
            'pass' not in wifidata['access_point_1']):
            self.skip("No AP found in the yaml config")

        self.interface = wifidata['wireless_interface']
        self.ap_ssid = wifidata['access_point_1']['ssid']
        self.ap_pass = wifidata['access_point_1']['pass']

    def test(self):
        self.connect_and_check()

    def connect_and_check(self):
        internet.connect(self.ap_ssid, self.ap_pass)
        time.sleep(4)
        gateway = internet.get_gateway(self.interface, self)

        pingResult = internet.pingtest_hard(gateway, self.interface, self)

        self.log.debug("Internet is working on network {0}".format(self.ap_ssid))
