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

        self.checkCon(accessPoint, accessPointPass)

    def checkCon(self, ssid, password):
        InternetUtils.connect(ssid, password)

        pingResult = InternetUtils.pingtest_hardfail('8.8.8.8', self.interface, self)

        self.log.debug("internet is working on network {0}".format(active))


