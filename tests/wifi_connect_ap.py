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

        if 'access_point_1' not in wifidata:
            self.skip("No AP found in the yaml config")

        if ('ssid' not in wifidata['access_point_1'] or
            'pass' not in wifidata['access_point_1']):
            self.skip("No AP found in the yaml config")

        self.ap_ssid = wifidata['access_point_1']['ssid']
        self.ap_pass = wifidata['access_point_1']['pass']

    def test(self):
        self.wireless_interface = internet.get_active_device('wifi', self)
        self.connect_and_check()

    def connect_and_check(self):
        internet.connect(self.ap_ssid, self.ap_pass)

        time.sleep(3)
        gateway = internet.get_gateway(self.wireless_interface, self)

        pingResult = internet.pingtest_hard("8.8.8.8", self.wireless_interface, self)

        self.log.debug("Internet is working on network {0}".format(self.ap_ssid))
