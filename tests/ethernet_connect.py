#!/usr/bin/env python
import subprocess as subp
import yaml
from utils import internet
from utils import utils

class EthernetConnect(Test):
    def test(self):
        internetdata = utils.load_yaml(self, "data/internet_data.yaml")

        self.interface = internetdata['wired_interface']

        gateway = internet.get_gateway(self.interface, self)

        pingResult = internet.pingtest_hard(gateway, self.interface)

        self.log.debug("Internet is working on ethernet interface {0}".format(self.interface))
