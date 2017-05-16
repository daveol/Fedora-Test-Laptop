from avocado import Test
from utils import internet
from utils import benzea_mon

class DisplayNativeResolution(Test):
    def test(self):
        mon = Gdk.Display.get_monitor(0)
        monitor = Monitor.from_monitor(mon)

        

        if monitor.width != expected_width or monitor.height != expected_height
            self.fail("Internal display did not match expected resolution")
