import os
import os.path
import glob
import time
import multiprocessing
import subprocess

from avocado import Test

HWMON_DIR = '/sys/class/hwmon'


def _cat(file_name):
    return open(file_name).read().strip()


class CpuTemps(Test):

    def setUp(self):
        self.__probes = glob.glob(
                os.path.join(HWMON_DIR, 'hwmon[0-9]/temp[1-9]_input')
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

        #check them
        for probe, temp in self.get_values().iteritems():
            if temp > 60:
                self.fail("%s is more than 60 degrees: %i", probe, temp)

    def test_load(self):
        """
        Test load temperatures
        """
        cores_idle = {}
        procs = []

        # Get idle results for cpu('s)
        for probe, temp in self.get_values().iteritems():
            label = probe.replace('input', 'label')
            if os.path.isfile(label):
                if 'CPU' in _cat(label):
                    cores_idle[probe] = temp

        if len(cores_idle.keys()) < 1:
            self.fail("no probes found with cpu label")
            return 1

        # Create cpu load
        for core in range(multiprocessing.cpu_count()):
            procs.append(subprocess.Popen(['sha256sum','/dev/random']))

        # Give some heat-up time
        time.sleep(20)

        # clean the processes
        for proc in procs:
            proc.kill()

        # test them again
        for probe, temp in self.get_values().iteritems():
            if probe in cores_idle.keys():
               if cores_idle[probe] + 5 < temp:
                   self.fail('No rise in temperature detected for %s', probe)
