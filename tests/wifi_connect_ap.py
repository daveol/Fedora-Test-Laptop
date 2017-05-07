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

    def tryCon(self, expected):
        # get the SSID connected on the interface
        p = subp.Popen(['iwgetid', self.interface, '-r'], stdout=subp.PIPE, stderr=subp.PIPE)

        stdout, stderr = p.communicate()
        activeCon = stdout.rstrip()

        if activeCon != expected:
            self.fail("initial network connection state was not as expected was: {0} expected {1}".format(activeCon, expected))
        self.log.debug("Current network checked. Now on {0}".format(activeCon))

        return activeCon

    def checkCon(self, ssid, password):
        InternetUtils.connect(ssid, password)

        active = self.tryCon(ssid)

        pingResult = InternetUtils.pingtest('8.8.8.8', self.interface)

        if pingResult == 0:
            self.log.debug("internet is working on network {0}".format(active))
        else:
            self.fail("Internet is not available on network {0}".format(active))


