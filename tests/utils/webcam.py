#!/usr/bin/env python

import gi, os
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gst

def create_video_pipeline(test_class):
    """
    Creates a pipeline using the default /dev/video0 webcam and a filesink
    cam.jpg. A signal watch is added to the bus, calling on_message when a
    message arrives. Set state to playing, causing the data to be rendered.

    :param test_class: The class which uses the video player

    """
    Gst.init([])
    img_path = os.path.join(test_class.logdir, 'cam.jpg')
    # using 10 buffers for webcam to adjust white balace values
    test_class.video_player = Gst.parse_launch("v4l2src num-buffers=10 ! jpegenc ! filesink location=" + img_path)

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
