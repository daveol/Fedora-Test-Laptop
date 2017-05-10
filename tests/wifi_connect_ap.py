#!/usr/bin/env python
import subprocess as subp
import yaml
from avocado import Test

from utils import internet
from utils import utils

class WifiConnectAP(Test):
    def test(self):
        wifidata = utils.load_yaml(self, "data/internet_data.yaml")

        accessPoint = wifidata['access_point_1']['ssid']
        accessPointPass = wifidata['access_point_1']['pass']
        self.interface = wifidata['wireless_interface']

        self.connect_and_check(accessPoint, accessPointPass)

    def connect_and_check(self, ssid, password):
        internet.connect(ssid, password)

        pingResult = internet.pingtest_hard('8.8.8.8', self.interface, self)

        self.log.debug("internet is working on network {0}".format(ssid))
