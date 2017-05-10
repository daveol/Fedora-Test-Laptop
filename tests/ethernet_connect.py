#!/usr/bin/env python
import subprocess as subp
import yaml
from internet_utils import InternetUtils
from avocado import Test

class EthernetConnect(Test):
    def test(self):
        internetdata = InternetUtils.load_yaml(self, "data/internet_data.yaml")

        self.interface = internetdata['wired_interface']

        self.connect_and_check()

    def connect_and_check(self):

        pingResult = InternetUtils.pingtest('8.8.8.8', self.interface)

        if pingResult != 0:
            self.fail("Internet is not available on ethernet interface {0}".format(self.interface))
        self.log.debug("internet is working on ethernet interface {0}".format(self.interface))
