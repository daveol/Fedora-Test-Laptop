#!/usr/bin/env python
import subprocess as subp
import yaml
from wifi_utils import WifiUtils
from avocado import Test

class WifiConnectAP(Test):
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
        knownNetworks = WifiUtils.get_known()

        stdout, stderr = knownNetworks.communicate()

        # something went wrong while getting the networks
        if stderr != "":
           self.fail("Getting known network list failed {0}".format(stderr))

        # each connection is seperated by '\n'
        connectionList = stdout.split("\n")
        existing = False

        """ 
        we check for the existance of the ssid in the known networks
        if the network ssid is found, it will connect using its UUID
        if not found, a new connection will be created and connected to
        """
        for con in connectionList:
            cParts = con.split(":") # nmcli -t output is seperated by :
            # see if the ssid exist, and has the correct type
            if ssid in cParts and cParts[3] == "802-11-wireless":
               existing = True
               if cParts[2] != "yes": # yes means active => don't reconnect
                  subp.call(['nmcli', 'con', 'up', 'uuid', cParts[1]]) # cParts[1] contains uuid

        # when the network does not yet exist, create a new one
        if existing == False:
            switch = subp.call(['nmcli', 'dev', 'wifi', 'con', ssid, 'password', password])        
        active = self.tryCon(ssid)
        #p = subp.call(['ping', '-I', self.interface, '8.8.8.8', '-c', '1'])
        pingResult = WifiUtils.pingtest('8.8.8.8', self.interface)

        if pingResult == 0:
            self.log.debug("internet is working on network {0}".format(active))
        else:
            self.fail("Internet is not available on network {0}".format(active))


