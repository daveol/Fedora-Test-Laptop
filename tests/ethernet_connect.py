#!/usr/bin/env python

from avocado import Test
from utils import internet, utils

class EthernetConnect(Test):
    """
    Uses the wired interface from internet_data to ping the default
    gateway using internet utils.
    
    """
    def setUp(self):
        self.wiredInterfaces = internet.get_interfaces('ethernet')

    def test(self):
        if len(self.wiredInterfaces) == 0:
            self.fail("No ethernet devices available")

        for interface in self.wiredInterfaces:
            gateway = internet.get_gateway(interface, self)

            pingResult = internet.pingtest_hard(gateway, interface, self)

            self.log.debug("Internet is working on ethernet interface {0}".format(interface))       
