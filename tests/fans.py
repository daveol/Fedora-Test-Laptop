import os
import os.path
import glob
import time
import multiprocessing
import subprocess
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


class Fans(Test):

    def setUp(self):
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
