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
import utils.cpu

from avocado import Test

HWMON_DIR = '/sys/class/hwmon'


def _cat(file_name, retry=3):
    while True:
        try:
            return open(file_name).read().strip()
        except IOError as error:
            if retry <= 0:
                raise error

            retry -= 1


class Fans(Test):
    """
    Testing them fans
    """

    def setUp(self):
        """
        Setup the tests
        """
        self.__probes = glob.glob(
            os.path.join(HWMON_DIR, 'hwmon*/fan*_input')
        )

        # Because weird drivers (Thinkpad)
        self.__probes.extend(glob.glob(
            os.path.join(HWMON_DIR, 'hwmon*/device/fan*_input')
        ))

        if len(self.__probes) < 1:
            self.skip('No fan monitoring found')

    def get_values(self):
        """
        Get the rpm from all the fans
        """
        fans = {}
        for fan in self.__probes:
            fans[fan] = int(_cat(fan))

        return fans

    def test_idle(self):
        """
        Test the idle fan speeds
        """
        # idle
        time.sleep(60)

        # check them
        for fan, rpm in self.get_values().iteritems():
            if rpm > 4000:
                self.fail("%s is more than 4000RPM in idle: %i", fan, rpm)

    def test_load(self):
        """
        Test the load fan speeds
        """
        speeds = {}

        # Get idle results for cpu('s)
        for probe, speed in self.get_values().iteritems():
            speeds[probe] = speed

        # Create cpu load
        utils.cpu.create_cpu_load()

        # test them again
        for probe, speed in self.get_values().iteritems():
            if speeds[probe] <= speed:
                self.fail('No rise in speed detected for %s', probe)
