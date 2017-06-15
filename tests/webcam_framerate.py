    #!/usr/bin/env python

import gi, os
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gst
from avocado import Test
from utils import webcam

class WebcamFrameRate(Test):
    """
    Uses the camera selected by v4l2src by default (/dev/video0) to get the
    framerate by creating a pipeline with an fpsdisplaysink and initializing
    Gtk main loop. The fpsdisplaysink element is retrieved from the pipeline
    to connect the fps-measurements signal to our on_fps_measurement method.
    For now is tested whether the framerate is 30 or more using 200 buffers.

    The element in test(), "video/x-raw, framerate=(rate)/1" can be changed
    when creating the pipeline. Where (rate) is the framerate, to test for
    different framerates if necessary.

    """
    def setUp(self):
        self.error = None
        if not os.path.exists('/dev/video0'):
            self.skip("No webcam detected: /dev/video0 cannot be found");

    def test(self):
        elements = ['video/x-raw, framerate=30/1',
                    'fpsdisplaysink video-sink=fakesink text-overlay=false '
                    'signal-fps-measurements=true']
        """
        num-buffers is set to 200, rounding the average fps to nearest int
        means .5/30 = 1.67% error margin. With 200 buffers 3 frames can be
        dropped before a fail.
        """
        webcam.create_video_pipeline(self, gst_elements=elements,
                                     v4l2src_args="num-buffers=200")

        fps_element = self.video_player.get_by_name("fpsdisplaysink0")
        fps_element.connect("fps-measurements", self.on_fps_measurement)

        Gtk.main()

        if self.error != None:
            self.fail("Error: {0}".format(self.error))

        if int(round(self.fps)) != 30:
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
