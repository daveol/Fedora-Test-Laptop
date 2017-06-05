#!/usr/bin/env python

"""
This module sets up a video stream from internal or connected webcam using Gstreamer.
You can then take snapshots.

import qrtools
qr = qrtools.QR()
qr.decode("cam.jpg")
print qr.data

"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk as gtk
from gi.repository import Gdk
from gi.repository import Gst as gst
from gi.repository import GdkPixbuf

from avocado import Test
from os.path import exists, relpath
import qrtools
import time

#import pyqrcode

class WebcamReadQR(Test):    
    def setUp(self):
        # if not exists('/dev/video0'):
            # self.skip("No webcam detected: /dev/video0 cannot be found");
        self.device = '/dev/video0'
        
        Gdk.threads_init()
        gtk.main()
        self.take_snapshot()

    def test(self):
        self.create_video_pipeline()
       
    def create_video_pipeline(self):
        gst.init([])
        #v4l2src
        self.video_player = gst.parse_launch("videotestsrc ! jpegenc ! filesink location=cam.jpg")
        self.video_player.set_state(gst.State.PLAYING)
        
        bus = self.video_player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        bus.enable_sync_message_emission()
        bus.connect("sync-message::element", self.on_sync_message)        

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MessageType.EOS:
            self.exit()
        elif t == gst.MessageType.ERROR:
            self.exit()
            self.fail("Error {0}".format(message.parse_error()))

    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
                   
    def exit(self):
        self.video_player.set_state(gst.State.NULL) 
        gtk.main_quit()
        
    def take_snapshot(self):
        #TODO:fill this in
