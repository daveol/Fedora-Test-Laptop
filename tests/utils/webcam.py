#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gdk, Gst

def create_video_pipeline(test_class):
    """
    Creates a pipeline using the default /dev/video0 webcam and a filesink
    cam.jpg. A signal watch is added to the bus, calling on_message when a 
    message arrives. Set state to playing, causing the data to be rendered.
    
    :param test_class: The class which uses the video player
    
    """
    Gst.init([])
    test_class.video_player = Gst.parse_launch("v4l2src num-buffers=10 ! jpegenc ! filesink location=cam.jpg")

    bus = test_class.video_player.get_bus()
    bus.add_signal_watch()
    bus.connect("message", test_class.on_message)
        
    test_class.video_player.set_state(Gst.State.PLAYING)

def exit(test_class):
    """
    Closes the device, quits the gtk main loop
    
    :param test_class: The class of which' video player to stop
    
    """
    test_class.video_player.set_state(Gst.State.NULL)
    Gtk.main_quit()
