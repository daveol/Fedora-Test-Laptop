#!/usr/bin/env python
import subprocess as subp
import yaml

from avocado import Test
from test import WifiTest

class WifiAPSwitch(WifiTest):
    """
    :avocado: enable
    """
    def test(self):
        with open("data/wifi_data.yaml", 'r') as stream:
            try:
                wifidata = yaml.load(stream)
            except yaml.YAMLError as exc:
                self.log.debug(exc)
        switchFrom = wifidata['access_point_1']['ssid']
        switchTo = wifidata['access_point_2']['ssid']
        switchFromPass = wifidata['access_point_1']['pass']
        switchToPass = wifidata['access_point_2']['pass']
        self.interface = wifidata['wireless_interface']

        self.switchCon(switchFrom, switchFromPass)
        self.switchCon(switchTo, switchToPass)


    def tryCon(self, expected):
        # get the SSID connected on the interface
        p = subp.Popen(['iwgetid', self.interface, '-r'], stdout=subp.PIPE, stderr=subp.PIPE)

        stdout, stderr = p.communicate()

        # trim extraneous whitespace
        activeCon = stdout.rstrip()

        if activeCon != expected:
            self.fail("initial network connection state was not as expected was: {0} expected {1}".format(activeCon, expected))
        self.log.debug("Current network checked. Now on {0}".format(activeCon))
        return activeCon

    def switchCon(self, ssid, password):
        # get all known networks
        p = subp.Popen(['nmcli', '-t', '--fields', 'NAME,UUID,ACTIVE,TYPE', 'c'], stdout=subp.PIPE, stderr=subp.PIPE)

        stdout, stderr = p.communicate()

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
        p = subp.call(['ping', '-I', self.interface, gateway, '-c', '1'])

        if p == 0:
            self.log.debug("Internet is working on network {0} pinged {1}".format(active, gateway))
        else:
            self.fail("Internet is not available on network {0} tried to ping {1}".format(active, gateway))

