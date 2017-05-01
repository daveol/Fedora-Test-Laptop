#!/usr/bin/env python
import subprocess as subp
import yaml
from avocado import Test

class WifiScanAP(Test):
    def test(self):
        with open("data/wifi_data.yaml", 'r') as stream:
            try:
                wifidata = yaml.load(stream)
            except yaml.YAMLError as exc:
                self.log.debug(exc)
        ap1 = wifidata['access_point_1']['ssid']
        ap2 = wifidata['access_point_2']['ssid']
        self.interface = wifidata['wireless_interface']

        self.scanAP(ap1, ap2);

    def scanAP(self, ap1, ap2):
        p = subp.Popen(['nmcli', 'device', 'wifi', 'list'], stdout=subp.PIPE, stderr=subp.PIPE)

        stdout, stderr = p.communicate()
        scan1 = stdout.rstrip()

        if ap1 not in scan1:
            self.fail("First AP not found {0}".format(ap1))
        if ap2 not in scan1:
            self.fail("Second AP not found {0}".format(ap2))
        else:
            self.log.debug("Both APs can be found")

