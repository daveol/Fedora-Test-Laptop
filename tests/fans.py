import os
import os.path
import glob
import time
import multiprocessing

from avocado import Test

HWMON_DIR = '/sys/class/hwmon'


def _cat(file_name):
    return open(file_name).read().strip()


class Fans(Test):

    def __init__(self):
        self.__probes = glob.glob(
                os.path.join(HWMON_DIR, 'hwmon[0-9]/fan[1-9]_input')
        )

    def get_values(self):
        fans = {}
        for fan in self.__probes:
            fans[fan] = _cat(fan)

        return fans

    def test_idle(self):
        if len(self.__probes):
            self.skip('No fan monitoring found')

        # be idle
        time.sleep(60)

        #check them
        for fan, rpm in self.get_values:
            if rpm > 4000:
                self.fail("%s is more than 4000RPM in idle: %i", fan, rpm)

    def test_load(self):
        if len(self.__probes) < 1:
            self.skip('No fan monitoring found')

        speeds = {}
        procs = []

        # Get idle results for cpu('s)
        for probe, speed in self.get_values():
            speeds[probe] = speed


        # Create cpu load
        for core in range(multiprocessing.cpu_count()):
            procs.append(subprocess.Popen(['sha256sum','/dev/random']))

        # Give some heat-up time
        time.sleep(20)

        # kill the load
        for proc in procs:
            proc.kill()

        # test them again
        for probe, speed in self.get_values():
            if speeds[probe] < speed:
                self.fail('No rise in speed detected for %s', probe)
