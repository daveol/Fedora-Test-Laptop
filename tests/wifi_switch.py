#!/usr/bin/env python
import subprocess as subp

from avocado import Test
from utils import internet
from utils import utils

class WifiSwitchAP(Test):
    def __init__(self):
        self.wifidata = utils.load_yaml(self, "data/internet_data.yaml")

    def test_switch_ap(self):
        wifidata = self.wifidata
        switchFrom = wifidata['access_point_1']['ssid']
        switchTo = wifidata['access_point_2']['ssid']
        switchFromPass = wifidata['access_point_1']['pass']
        switchToPass = wifidata['access_point_2']['pass']
        self.interface = wifidata['wireless_interface']

        self.switch_con(switchFrom, switchFromPass)
        self.switch_con(switchTo, switchToPass)
        
    def test_switch_freq(self):
        wifidata = self.wifidata
        switchFrom = wifidata['access_point_1']['ssid']
        switchTo = wifidata['access_point_5ghz']['ssid']
        switchFromPass = wifidata['access_point_1']['pass']
        switchToPass = wifidata['access_point_5ghz']['pass']
        self.interface = wifidata['wireless_interface']

        self.switch_con(switchFrom, switchFromPass)
        self.switch_con(switchTo, switchToPass)

    def switch_con(self, ssid, password):		
        internet.connect(ssid, password)

        # get the default gateway by parsing ip route's output
        gatewayP1 = subp.Popen(['ip', 'route'], stdout=subp.PIPE, stderr=subp.PIPE)
        gatewayP2 = subp.Popen(['awk', r'/default/ { print $3 }'], stdin=gatewayP1.stdout, stdout=subp.PIPE, stderr=subp.PIPE)

        gateway, stderr = gatewayP2.communicate()

        # something went wrong while getting the gateway
        if stderr != "":
           self.fail("Getting gateway failed {0}".format(stderr))

        # ping default gateway using the desired interface once then check for success
        success = internet.pingtest(gateway, self.interface)

        if success == 0:
            self.fail("Internet is not available on network {0}, tried to ping {1}".format(ssid, gateway))
        self.log.debug("Internet is working on network {0}, pinged {1}".format(ssid, gateway))
            


