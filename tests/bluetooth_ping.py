#!/usr/bin/env python
import os
import subprocess as subp
from avocado import Test
from utils import utils
import re


class BluetoothPing(Test):
    '''
    This test will ping a specific device. The device needs to be specified in the
    YAML file. If the device responds, the result will be found in the debug log.
    If the test fails, a fail exception will be raised.
    '''
    def setUp(self):
        try:
            self.targetDeviceMac = self.testdata['testdata']['addr']
        except:
            self.skip('Invalid testdata')

        if not bool(re.match('^' + '[\:\-]'.join(['([0-9a-f]{2})']*6) + '$', self.targetDeviceMac.lower())):
            self.skip('Target Device mac address invalid')

    def test(self):      
        p = self.pingtest()
        
        if p != 0 :
            self.fail("Could not ping " + self.targetDeviceMac)
        

    def pingtest(self):
        p= subp.Popen(['pkexec', 'l2ping', self.targetDeviceMac ,'-c', '5'], stdout=subp.PIPE, stderr=subp.PIPE)
        result = p.communicate()[0]
        returnCode = p.returncode
        self.log.debug("Ping test working {0}".format(result))
        return returnCode
