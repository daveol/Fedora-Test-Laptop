#!/usr/bin/env python

from avocado import Test
from utils import internet, utils

class EthernetConnect(Test):
    """
    Uses the wired interface from internet_data to ping the default
    gateway using internet utils.

    """
    def test(self):
        wired_interface = internet.get_active_device('ethernet', self)
        w_iface = wired_interface.get_iface()

        gateway = internet.get_gateway(w_iface, self)

        pingResult = internet.pingtest_hard(gateway, w_iface, self)

        self.log.debug("Internet is working on ethernet interface {0}"
                       .format(w_iface))
