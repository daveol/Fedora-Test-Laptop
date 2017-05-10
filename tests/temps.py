import os
import os.path
import glob
import time

from avocado import Test

HWMON_DIR = '/sys/class/hwmon'


def _cat(file_name):
    return open(file_name).read().strip()


class Temperatures(Test):

    def __init__(self):
        self.__probes = glob.glob(
                os.path.join(HWMON_DIR, 'hwmon[0-9]/temp[1-9]_input')
        )

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
        # be idle
        time.sleep(60)

        #check them
        for probe, temp in self.get_values():
            if temp < 60:
                self.fail("%s is more than 60 degrees: %i", probe, temp)

    def test_load(self):
        self.fail("todo: implement")
