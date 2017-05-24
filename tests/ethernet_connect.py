#!/usr/bin/env python

from avocado import Test
from utils import internet, utils

class EthernetConnect(Test):
    """
    Uses the wired interface from internet_data to ping the default
    gateway using internet utils.
    
    """
    def setUp(self):
        self.internetdata = utils.load_yaml(self, "data/internet_data.yaml")
        
        if 'wired_interface' not in wifidata:
            self.skip("No wired interface in the yaml config")
            
        self.interface = internetdata['wired_interface']
    
    def test(self):
        gateway = internet.get_gateway(self.interface, self)

        pingResult = internet.pingtest_hard(gateway, self.interface, self)

        self.log.debug("Internet is working on ethernet interface {0}".format(self.interface))
