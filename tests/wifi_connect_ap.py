#!/usr/bin/env python

from avocado import Test
from utils import internet, utils

class WifiConnectAP(Test):
    """
    Uses the first access point from internet_data to ping the default
    gateway using internet utils.

    """
    def setUp(self):
        wifidata = utils.load_yaml(self, "data/internet_data.yaml")

        if 'access_point_1' not in wifidata:
            self.skip("No AP found in the yaml config")

        if ('ssid' not in wifidata['access_point_1'] or
            'pass' not in wifidata['access_point_1']):
            self.skip("No AP found in the yaml config")

        wireless_if = internet.get_interfaces('wifi')

        if len(wireless_if) == 0:
            self.skip("No wireless interface found")

        self.interface = wireless_if[0]
        self.ap_ssid = wifidata['access_point_1']['ssid']
        self.ap_pass = wifidata['access_point_1']['pass']

    def test(self):
        self.connect_and_check()

    def connect_and_check(self):
        internet.connect(self.ap_ssid, self.ap_pass)

        gateway = internet.get_gateway(self.interface, self)

        pingResult = internet.pingtest_hard(gateway, self.interface, self)

        self.log.debug("Internet is working on network {0}".format(self.ap_ssid))
