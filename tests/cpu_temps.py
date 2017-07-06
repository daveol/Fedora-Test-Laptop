# Copyright (C) 2017 Dave Olsthoon <dave@bewaar.me>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os
import os.path
import glob
import time
import re
import utils.cpu

from avocado import Test

HWMON_DIR = '/sys/class/hwmon'


def _cat(file_name, retry=3):
    while True:
        try:
            return open(file_name).read().strip()
        except IOError as e:
            if retry <= 0:
                raise e

            retry -= 1


class CpuTemps(Test):

    def setUp(self):
        """
        Figure out which temperature probes exist
        """
        self.__probes = glob.glob(
                os.path.join(HWMON_DIR, 'hwmon*/temp*_input')
        )

        if len(self.__probes) < 1:
            self.skip('No probes found')
            return 1

    def get_values(self):
        """
        Get the temperature of the probes in the device

        returns an dict with path and temperatures
        """
        temperatures = {}

        # Iterate over probes
        for probe in self.__probes:
            # Get the temperature
            temperatures[probe] = int(_cat(probe))/1000

        return temperatures

    def test_idle(self):
        """
        Test idle temperatures
        """
        # be idle
        time.sleep(60)

        # check them
        for probe, temp in self.get_values().iteritems():
            if temp > 60:
                self.fail("%s is more than 60 degrees: %i", probe, temp)

    def test_load(self):
        """
        Test load temperatures
        """
        cores_idle = {}
        regex = re.compile("(CPU|Package|Core)")

        # Get idle results for cpu('s)
        for probe, temp in self.get_values().iteritems():
            label = probe.replace('input', 'label')
            if os.path.isfile(label):
                if regex.match(_cat(label)):
                    cores_idle[probe] = temp

        if len(cores_idle.keys()) < 1:
            self.fail("no probes found with cpu label")
            return 1

        # Create cpu load
        utils.cpu.create_cpu_load()

        # test them again
        for probe, temp in self.get_values().iteritems():
            if probe in cores_idle.keys():
                if cores_idle[probe] + 5 < temp:
                    self.fail('No rise in temperature detected for %s', probe)
