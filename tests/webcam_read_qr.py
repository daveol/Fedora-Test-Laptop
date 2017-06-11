#!/usr/bin/env python

import qrtools, gi, os
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gst

from avocado import Test
from utils import webcam
import time

class WebcamReadQR(Test):
    """
    Uses the camera selected by v4l2src by default (/dev/video0) to read
    QR data by creating a pipeline, initializing Gtk main loop, and checking
    if the decoded data from the QR code is correct after receiving the EOS
    message. The .jpg is saved in the self.logdata directory.

    """
    def setUp(self):
        self.error = None
        self.qr_data = None
        if not os.path.exists('/dev/video0'):
            self.skip("No webcam detected: /dev/video0 cannot be found");

    def test(self):
        webcam.create_video_pipeline(self)
        Gtk.main()

        if self.error != None:
            self.fail("Error: {0}".format(self.error))

        if self.qr_data != "test":
            self.fail("QR code was not read properly")
        self.log.debug("QR code was read properly")

    def on_message(self, bus, message):
        img_path = os.path.join(self.logdir, 'cam.jpg')
        t = message.type

        if t == Gst.MessageType.EOS:
            webcam.exit(self)

            qr = qrtools.QR()
            qr.decode(img_path)
            self.log.debug("Read QR data: {0}".format(qr.data))
            self.qr_data = qr.data

        elif t == Gst.MessageType.ERROR:
            webcam.exit(self)
            self.error = message.parse_error()
