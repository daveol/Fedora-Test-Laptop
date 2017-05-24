#!/usr/bin/env python

from avocado import Test
from utils import internet, utils

class WifiSwitchAP(Test):
    """
    First, the two first access points are loaded from internet_data. The first
    access point will be used to test the connection, then the second one, to
    test a switch of access point.
    Secondly, the first and 5GHz access points are loaded from internet_data. The
    test sequence remains the same as in the first test.

    """
    def setUp(self):
        wifidata = utils.load_yaml(self, "data/internet_data.yaml")

        if 'wireless_interface' not in wifidata:
            self.skip("No wireless interface in the yaml config")

        if 'access_point_1' not in wifidata:
            self.skip("First AP not found in the yaml config")

        if ('ssid' not in wifidata['access_point_1'] or
            'pass' not in wifidata['access_point_1']):
            self.skip("First AP data not found in the yaml config")

        if 'access_point_2' not in wifidata:
            self.skip("Second AP not found in the yaml config")

        if ('ssid' not in wifidata['access_point_2'] or
            'pass' not in wifidata['access_point_2']):
            self.skip("Second AP data not found in the yaml config")

        if 'access_point_5ghz' not in wifidata:
            self.skip("5GHz AP not found in the yaml config")

        if ('ssid' not in wifidata['access_point_5ghz'] or
            'pass' not in wifidata['access_point_5ghz']):
            self.skip("5GHz AP data not found in the yaml config")

        self.interface = wifidata['wireless_interface']
        self.ap1_ssid = wifidata['access_point_1']['ssid']
	    self.ap1_pass = wifidata['access_point_1']['pass']
	    self.ap2_ssid = wifidata['access_point_2']['ssid']
	    self.ap2_pass = wifidata['access_point_2']['pass']
	    self.ap5ghz_ssid = wifidata['access_point_5ghz']['ssid']
	    self.ap5ghz_pass = wifidata['access_point_5ghz']['pass']

    def test_switch_ap(self):
        self.switch_con(self.ap1_ssid, self.ap1_pass)
        self.switch_con(self.ap2_ssid, self.ap2_pass)

    def test_switch_freq(self):
        self.switch_con(self.ap1_ssid, self.ap1_pass)
        self.switch_con(self.ap5ghz_ssid, self.ap5ghz_pass)

    def switch_con(self, ssid, password):
        internet.connect(ssid, password)

        gateway = internet.get_gateway(self.interface, self)

        internet.pingtest_hard(gateway, self.interface, self)

        self.log.debug("Internet is working on network {0}, pinged {1}".format(ssid, gateway))
