#!/usr/bin/env python

from avocado import Test
from utils import internet, utils

class RadioKill(Test):
    def test(self):
        wifidata = utils.load_yaml(self, "data/internet_data.yaml")

        accessPoint = wifidata['access_point_1']['ssid']
        accessPointPass = wifidata['access_point_1']['pass']
        self.interface = wifidata['wireless_interface']

        self.block_and_verify(accessPoint, accessPointPass)

    def block_and_verify(self, ssid, password):
        p = subp.call(['rfkill', 'block', 'all'])     

        internet.connect(ssid, password)
        gateway = internet.get_gateway(self.interface, self)
        pingResult = internet.pingtest(gateway, self.interface)

        if(pingResult == True)
            self.fail("Wi-Fi still works despite radio kill on network {0}".format(ssid))
        
    
