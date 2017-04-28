#!/usr/bin/env python
import subprocess as subp
from avocado import Test

class WifiTest(Test):

    def test(self):
        switch1 = subp.call(['nmcli', 'dev', 'wifi', 'con', 'nick', 'password', 'yoloyolo'])

        p = subp.call(['ping', '-I', 'wlan0', '8.8.8.8', '-c', '1'])

        if p == 0:
            self.log.debug("internet is working")
        else:
            self.fail("Internet is not available")

        switch2 = subp.call(['nmcli', 'dev', 'wifi', 'con', 'nasakeni', 'password', 'mzsv1425'])

        p2 = subp.call(['ping', '-I', 'wlan0', '8.8.8.8', '-c', '1'])

        if p2 == 0:
            self.log.debug("internet is working %s")
        else:
            self.fail("Internet is not available")
