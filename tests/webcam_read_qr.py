#!/usr/bin/env python

"""
This module sets up a video stream from internal or connected webcam using Gstreamer.
You can then take snapshots.


"""
import qrtools
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gdk, Gst

from avocado import Test
from os.path import exists, relpath
from utils import webcam
import time

class WebcamReadQR(Test):
    """
    Uses the internal webcam /dev/video0 to read QR data by creating a 
    pipeline, initializing Gtk main loop, and checking if the decoded data
    from the QR code is correct after receiving the EOS message.
    
    """
    def setUp(self):
        if not exists('/dev/video0'):
            self.skip("No webcam detected: /dev/video0 cannot be found");

    def test(self):
        webcam.create_video_pipeline(self)
        Gdk.threads_init()
        Gtk.main()

        if (self.qr_data != "test"):
            self.fail("QR code was not read properly")
        self.log.debug("QR code was read properly")

    def on_message(self, bus, message):
        t = message.type

        if t == Gst.MessageType.EOS:
            webcam.exit(self)

            time.sleep(3)
            qr = qrtools.QR()
            qr.decode("cam.jpg")
            self.log.debug(qr.data)
            self.qr_data = qr.data
        elif t == Gst.MessageType.ERROR:
            webcam.exit(self)
            self.fail("Error {0}".format(message.parse_error()))
