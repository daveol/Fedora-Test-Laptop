#!/usr/bin/env python

from avocado import Test
from utils import internet, utils

class WifiConnectAP(Test):
    """
    Uses the first access point from internet_data to ping the default
    gateway using internet utils.
    
    """
    def test(self):
        wifidata = utils.load_yaml(self, "data/internet_data.yaml")

        accessPoint = wifidata['access_point_1']['ssid']
        accessPointPass = wifidata['access_point_1']['pass']
        self.interface = wifidata['wireless_interface']

        self.connect_and_check(accessPoint, accessPointPass)

    def connect_and_check(self, ssid, password):
        internet.connect(ssid, password)

        gateway = internet.get_gateway(self.interface, self)

        pingResult = internet.pingtest_hard(gateway, self.interface, self)

        self.log.debug("Internet is working on network {0}".format(ssid))
