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
import time

class WebcamReadQR(Test):
    def setUp(self):
        # if not exists('/dev/video0'):
            # self.skip("No webcam detected: /dev/video0 cannot be found");
        self.device = '/dev/video0'

        self.take_snapshot()

    def test(self):
        self.create_video_pipeline()
        Gdk.threads_init()
        Gtk.main()
        if (self.qr_data != "test"):
            self.fail(3)

    def create_video_pipeline(self):
        Gst.init([])
        #v4l2src
        self.video_player = Gst.parse_launch("v4l2src num-buffers=10 ! jpegenc ! filesink location=cam_f.jpg")

        bus = self.video_player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        self.video_player.set_state(Gst.State.PLAYING)

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.exit()

            time.sleep(3)
            qr = qrtools.QR()
            qr.decode("cam.jpg")
            self.log.debug(qr.data)
            self.qr_data = qr.data
        elif t == Gst.MessageType.ERROR:
            self.exit()
            self.fail("Error {0}".format(message.parse_error()))

    def exit(self):
        self.video_player.set_state(Gst.State.NULL)
        Gtk.main_quit()

    def take_snapshot(self):
        pass
        #TODO:fill this in, probably with set state to PLAYING
