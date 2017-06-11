#!/usr/bin/env python

import qrtools, gi, os
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gst

from avocado import Test
from utils import webcam

class WebcamReadQR(Test):
    """
    Uses the camera selected by v4l2src by default (/dev/video0) to read
    QR data by creating a pipeline, initializing Gtk main loop, and checking
    if the decoded data from the QR code is correct after receiving the EOS
    message. The .jpg is saved in the self.logdata directory.

    For now, has a manual tag because a QR code needs to be presented to
    pass. This can just be a piece of paper with the QR printed on it.

    :avocado: tags=manual
    """
    def setUp(self):
        self.error = None
        self.qr_data = None

        if not os.path.exists('/dev/video0'):
            self.skip("No webcam detected: /dev/video0 cannot be found")

        self.img_path = os.path.join(self.logdir, 'cam.jpg')

    def test_raw_image(self):
        elements = ['jpegenc', 'filesink location=' + self.img_path]
        webcam.create_video_pipeline(self, gst_elements=elements)
        Gtk.main()

        if self.error != None:
            self.fail("Error: {0}".format(self.error))

        if self.qr_data != "test":
            self.fail("QR code was not read properly")
        self.log.debug("QR code was read properly")

    def test_single_mirrored(self):
        elements = ['videoflip method=horizontal-flip',
                    'jpegenc', 'filesink location=' + self.img_path]
        webcam.create_video_pipeline(self, gst_elements=elements)
        Gtk.main()

        if self.error != None:
            self.fail("Error: {0}".format(self.error))

        if self.qr_data != "NULL":
            self.fail("QR code was read after single horizontal-flip")
        self.log.debug("QR code not read after horizontal-flip")

    def test_double_mirrored(self):
        elements = ['videoflip method=horizontal-flip',
                    'videoflip method=horizontal-flip',
                    'jpegenc', 'filesink location=' + self.img_path]
        webcam.create_video_pipeline(self, gst_elements=elements)
        Gtk.main()

        if self.error != None:
            self.fail("Error: {0}".format(self.error))

        if self.qr_data != "test":
            self.fail("QR code was not read properly after two horizontal-flips")
        self.log.debug("QR code was read properly after two horizontal-flips")

    def on_message(self, bus, message):
        t = message.type

        if t == Gst.MessageType.EOS:
            webcam.exit(self)

            qr = qrtools.QR()
            qr.decode(self.img_path)
            self.log.debug("Read QR data: {0}".format(qr.data))
            self.qr_data = qr.data

        elif t == Gst.MessageType.ERROR:
            webcam.exit(self)
            self.error = message.parse_error()
