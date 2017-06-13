#!/usr/bin/env python

import qrtools, gi, os
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gst
from avocado import Test
from utils import webcam

class WebcamReadQR(Test):
    """
    Uses the camera selected by v4l2src by default (/dev/video0) to get the
    framerate by creating a pipeline with an fpsdisplaysink and initializing
    Gtk main loop. The fpsdisplaysink element is retrieved from the pipeline
    to connect the fps-measurements signal to our on_fps_measurement method.
    For now is tested whether the framerate is 30 or more using 100 buffers.

    For testing purposes, " ! video/x-raw, framerate=30/1" can be added with
    v4l2src_args when creating the pipeline.

    """
    def setUp(self):
        self.error = None
        if not os.path.exists('/dev/video0'):
            self.skip("No webcam detected: /dev/video0 cannot be found");

    def test(self):
        elements = ['fpsdisplaysink video-sink=fakesink text-overlay=false '
                    'signal-fps-measurements=true']
        webcam.create_video_pipeline(self, gst_elements=elements,
                                     v4l2src_args=" num-buffers=100")

        fps_element = self.video_player.get_by_name("fpsdisplaysink0")
        fps_element.connect("fps-measurements", self.on_fps_measurement)

        Gtk.main()

        if self.error != None:
            self.fail("Error: {0}".format(self.error))

        if self.fps < 30:
            self.fail("Measured fps is below 30, {0}".format(self.fps))
        self.log.debug("Measured fps is 30 or more, {0}".format(self.fps))

    def on_fps_measurement(self, fpsdisplaysink, fps, droprate, avgfps):
        self.fps = avgfps

    def on_message(self, bus, message):
        t = message.type

        if t == Gst.MessageType.EOS:
            webcam.exit(self)

        elif t == Gst.MessageType.ERROR:
            webcam.exit(self)
            self.error = message.parse_error()
