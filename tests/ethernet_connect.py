#!/usr/bin/env python

# Copyright 2017 Nick Dekker, Marthe Veldhuis.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see LICENSE.txt.

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
