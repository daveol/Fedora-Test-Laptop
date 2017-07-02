#!/usr/bin/env python

# Copyright 2017 Nick Dekker.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see LICENSE.txt.

from avocado import Test

from utils import utils
from utils.monitor import Monitor
from utils.hwinfo import HWinfo
"""
above 2 lines were files imported from 
benzea repo -- later adoption should use:
"""
#from fed_laptoptest.monitors import Monitor
#from fed_laptoptest.hwinfo import HWinfo

from gi.repository import Gtk, Gdk, GLib

class DisplayNativeResolution(Test):
    """
    Gets the current resolution of the screen and
    tests the value against the expected value
    gathered from data/resolutions.yaml

    TODO: find a better way to fetch monitor res

    :avocado: tags=display
    """
    def setUp(self):
        resolutions = utils.load_yaml(self, "data/resolutions.yaml")

        hwinfo = HWinfo()

        try:
            hwinfo_data     = hwinfo.dmi_load()
            manufacturer    = hwinfo_data['sys_vendor'].lower()
            model           = hwinfo_data['product_name'].lower()
            self.log.debug(
                'checking for graphics device "%s" from vendor "%s"',
                manufacturer,
                model
            )
            if manufacturer not in resolutions:
                for manu in resolutions:
                    manu = manu.lower()
                    if manufacturer in manu or manu in manufacturer:
                        manufacturer = manu

            self.expected_width  = int(resolutions[manufacturer][model]['width'])
            self.expected_height = int(resolutions[manufacturer][model]['height'])

        except:
            self.skip('Screen info not found')

    def test(self):

        mon     = Gdk.Display.get_monitor(Gdk.Display.get_default(), 0)
        monitor = Monitor.from_monitor(mon)

        hwinfo = HWinfo()

        hwinfo_data     = hwinfo.dmi_load()
        manufacturer    = hwinfo_data['sys_vendor'].lower()
        model           = hwinfo_data['product_name'].lower()

        expected_width  = self.expected_width
        expected_height = self.expected_height

        if monitor.width != expected_width or monitor.height != expected_height:
            self.fail(
                "Internal display did not match expected resolution, expected: "
                "{0}x{1} got: {2}x{3}".format(expected_width, expected_height,
                monitor.width, monitor.height))
