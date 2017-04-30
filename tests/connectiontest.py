#!/usr/bin/env python
import subprocess as subp
import yaml
from avocado import Test

class WifiTest_ConnectAP(Test):
    def test(self):
        with open("data/wifi_data.yaml", 'r') as stream:
            try:
                wifidata = yaml.load(stream)
            except yaml.YAMLError as exc:
                self.log.debug(exc)
        accessPoint = wifidata['access_point_1']['ssid']
        accessPointPass = wifidata['access_point_1']['pass']
        self.interface = wifidata['wireless_interface']

        self.checkCon(accessPoint, accessPointPass)

    def tryCon(self, expected):
        # get the SSID connected on the interface
        p = subp.Popen(['iwgetid', self.interface, '-r'], stdout=subp.PIPE, stderr=subp.PIPE)

        stdout, stderr = p.communicate()
        activeCon = stdout.rstrip()

        if activeCon != expected:
            self.fail("initial network connection state was not as expected was: {0} expected {1}".format(activeCon, expected))
        self.log.debug("Current network checked. Now on {0}".format(activeCon))
        return activeCon

    def checkCon(self, ssid, password):
        check = subp.call(['nmcli', 'dev', 'wifi', 'con', ssid, 'password', password])
        
        active = self.tryCon(ssid)
        p = subp.call(['ping', '-I', self.interface, '8.8.8.8', '-c', '1'])
        
        if p == 0:
            self.log.debug("internet is working on network {0}".format(active))
        else:
            self.fail("Internet is not available on network {0}".format(active))

