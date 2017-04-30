from avocado import Test
from avocado import main
from avocado.core import exceptions
from avocado.core import sysinfo

class WifiTest(Test):
    """ 
    Should be integrated in fed_laptoptest/test.py

    A base class for tests which use the network connection to monitor
    kernel events with an iw event profiler.

    To use this class you need to set the avocado enable flag in the test.
    """

    def setUp(self):
        #sysinfo.SysInfo.add_cmd("iw event -t","start_job")
    def tearDown(self):
        pass
