from avocado import Test

from utils import utils

from utils.monitor import Monitor
from utils.hwinfo import HWinfo
#from fed_laptoptest.monitors import Monitor
#from fed_laptoptest.hwinfo import HWinfo

from gi.repository import Gtk, Gdk, GLib

class DisplayNativeResolution(Test):
    """
    pass

    :avocado: tags=display
    """
    def test(self):
        resolutions = utils.load_yaml(self, "data/resolutions.yaml")

        mon     = Gdk.Display.get_monitor(Gdk.Display.get_default(), 0)
        monitor = Monitor.from_monitor(mon)

        hwinfo = HWinfo()

        hwinfo_data     = hwinfo.dmi_load()
        manufacturer    = hwinfo_data['sys_vendor'].lower()
        model           = hwinfo_data['product_name'].lower()
        
        if manufacturer not in resolutions:
            for manu in resolutions:
                manu = manu.lower()
                if manufacturer in manu or manu in manufacturer:
                    manufacturer = manu

        expected_width  = int(resolutions[manufacturer][model]['width'])
        expected_height = int(resolutions[manufacturer][model]['height'])

        if monitor.width != expected_width or monitor.height != expected_height:
            self.fail("Internal display did not match expected resolution expected {0}x{1} got {2}x{3}".format(
            expected_width, expected_height, monitor.width, monitor.height))
