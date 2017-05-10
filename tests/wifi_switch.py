#!/usr/bin/env python
import subprocess as subp

from avocado import Test
from internet_utils import InternetUtils

class WifiSwitchAP(Test):
    def test_switch_ap(self):
        wifidata = InternetUtils.load_yaml(self, "data/internet_data.yaml")
        switchFrom = wifidata['access_point_1']['ssid']
        switchTo = wifidata['access_point_2']['ssid']
        switchFromPass = wifidata['access_point_1']['pass']
        switchToPass = wifidata['access_point_2']['pass']
        self.interface = wifidata['wireless_interface']

        self.switchCon(switchFrom, switchFromPass)
        self.switchCon(switchTo, switchToPass)
        
    def test_switch_feq(self):
        wifidata = InternetUtils.load_yaml(self, "data/internet_data.yaml")
        switchFrom = wifidata['access_point_1']['ssid']
        switchTo = wifidata['access_point_5ghz']['ssid']
        switchFromPass = wifidata['access_point_1']['pass']
        switchToPass = wifidata['access_point_5ghz']['pass']
        self.interface = wifidata['wireless_interface']

        self.switchCon(switchFrom, switchFromPass)
        self.switchCon(switchTo, switchToPass)

    def switch_con(self, ssid, password):		
        InternetUtils.connect(ssid, password)

        # get the default gateway by parsing ip route's output
        gatewayP1 = subp.Popen(['ip', 'route'], stdout=subp.PIPE, stderr=subp.PIPE)
        gatewayP2 = subp.Popen(['awk', r'/default/ { print $3 }'], stdin=gatewayP1.stdout, stdout=subp.PIPE, stderr=subp.PIPE)

        gateway, stderr = gatewayP2.communicate()

        # something went wrong while getting the gateway
        if stderr != "":
           self.fail("Getting gateway failed {0}".format(stderr))

        # ping default gateway using the desired interface once then check for success
        pingResult = InternetUtils.pingtest(gateway, self.interface)

        if pingResult != 0:
            self.fail("Internet is not available on network {0}, tried to ping {1}".format(ssid, gateway))
        self.log.debug("Internet is working on network {0}, pinged {1}".format(ssid, gateway))
            


