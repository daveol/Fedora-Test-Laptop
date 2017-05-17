#!/usr/bin/env python

from avocado import Test
from utils import internet, utils

class EthernetConnect(Test):
    """
    Uses the wired interface from internet_data to ping the default
    gateway using internet utils.
    
    """
    def test(self):
        internetdata = utils.load_yaml(self, "data/internet_data.yaml")

        self.interface = internetdata['wired_interface']

        gateway = internet.get_gateway(self.interface, self)

        pingResult = internet.pingtest_hard(gateway, self.interface, self)

        self.log.debug("Internet is working on ethernet interface {0}".format(self.interface))
