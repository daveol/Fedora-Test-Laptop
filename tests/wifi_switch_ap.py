#!/usr/bin/env python
import subprocess as subp

from avocado import Test
from internet_utils import InternetUtils

class WifiSwitchAP(Test):
    def test(self):
        wifidata = InternetUtils.load_yaml(self, "data/wifi_data.yaml")
        switchFrom = wifidata['access_point_1']['ssid']
        switchTo = wifidata['access_point_2']['ssid']
        switchFromPass = wifidata['access_point_1']['pass']
        switchToPass = wifidata['access_point_2']['pass']
        self.interface = wifidata['wireless_interface']

        self.switchCon(switchFrom, switchFromPass)
        self.switchCon(switchTo, switchToPass)
    def tryCon(self, expected):
        # get the SSID connected on the interface
        #p = subp.Popen(['iwgetid', self.interface, '-r'], stdout=subp.PIPE, stderr=subp.PIPE)

        #stdout, stderr = p.communicate()

        # trim extraneous whitespace
        activeCon = InternetUtils.connected_to(self.interface) #stdout.rstrip()

        if activeCon != expected:
            self.fail("initial network connection state was not as expected was: {0} expected {1}".format(activeCon, expected))
        self.log.debug("Current network checked. Now on {0}".format(activeCon))
        return activeCon

    def switchCon(self, ssid, password):		
        InternetUtils.connect(ssid, password)

        # see if the actual connection is still the same as expected
        active = self.tryCon(ssid)

        # get the default gateway by parsing ip route's output
        gatewayP1 = subp.Popen(['ip', 'route'], stdout=subp.PIPE, stderr=subp.PIPE)
        gatewayP2 = subp.Popen(['awk', r'/default/ { print $3 }'], stdin=gatewayP1.stdout, stdout=subp.PIPE, stderr=subp.PIPE)

        gateway, stderr = gatewayP2.communicate()

        # something went wrong while getting the gateway
        if stderr != "":
           self.fail("Getting gateway failed {0}".format(stderr))

        # ping default gateway using the desired interface once then check for success
        #pingResult = subp.call(['ping', '-I', self.interface, gateway, '-c', '1'])
        pingResult = InternetUtils.pingtest(gateway, self.interface)

        if pingResult == 0:
            self.log.debug("Internet is working on network {0}, pinged {1}".format(active, gateway))
        else:
            self.fail("Internet is not available on network {0}, tried to ping {1}".format(active, gateway))


