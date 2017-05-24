#!/usr/bin/env python

import subprocess as subp
from avocado import Test
from utils import utils

class WifiScanAP(Test):
    """
    Gets the first two access points in internet_data and scans the 
    network to find these.
    
    """
    def setUp(self):
        self.wifidata = utils.load_yaml(self, "data/internet_data.yaml")
        
        if 'access_point_1' not in wifidata:
            self.skip("First AP not found in the yaml config")

        if 'access_point_2' not in wifidata:
            self.skip("Second AP not found in the yaml config")

        self.ap1_ssid = wifidata['access_point_1']['ssid']
        self.ap2_ssid = wifidata['access_point_2']['ssid']
    
    def test(self):
        self.scan_ap();

    def scan_ap(self):        
        p = subp.Popen(['nmcli', 'device', 'wifi', 'list'], stdout=subp.PIPE, stderr=subp.PIPE)

        stdout, stderr = p.communicate()
        scan1 = stdout

        if self.ap1_ssid not in scan1:
            self.fail("First AP not found {0}".format(self.ap1_ssid))
        if self.ap2_ssid not in scan1:
            self.fail("Second AP not found {0}".format(self.ap2_ssid))
        self.log.debug("Both APs can be found")

