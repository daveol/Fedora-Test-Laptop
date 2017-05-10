#!/usr/bin/env python
import subprocess as subp
import yaml
from internet_utils import InternetUtils
from avocado import Test

class WifiConnectAP(Test):
    def test(self):
        wifidata = InternetUtils.load_yaml(self, "data/internet_data.yaml")

        accessPoint = wifidata['access_point_1']['ssid']
        accessPointPass = wifidata['access_point_1']['pass']
        self.interface = wifidata['wireless_interface']

        self.connect_and_check(accessPoint, accessPointPass)

    def connect_and_check(self, ssid, password):
        InternetUtils.connect(ssid, password)

        pingResult = InternetUtils.pingtest('8.8.8.8', self.interface)

        if pingResult != 0:
            self.fail("Internet is not available on network {0}".format(ssid))
        self.log.debug("Internet is working on network {0}".format(ssid))
