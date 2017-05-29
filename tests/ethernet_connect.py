#!/usr/bin/env python

from avocado import Test
from utils import internet, utils

class EthernetConnect(Test):
    """
    Uses the wired interface from internet_data to ping the default
    gateway using internet utils.

    """
    def test(self):
            self.wired_interface = internet.get_active_interface('ethernet', self)

            gateway = internet.get_gateway(self.wired_interface, self)

            pingResult = internet.pingtest_hard(gateway, self.wired_interface, self)

            self.log.debug("Internet is working on ethernet interface {0}".format(wired_interface))
