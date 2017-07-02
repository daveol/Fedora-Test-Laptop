#!/usr/bin/env python

# Copyright 2017 Nick Dekker, Marthe Veldhuis.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see LICENSE.txt.

import gi, os
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gst

def create_video_pipeline(test_class, gst_elements, v4l2src_args="", seperator="!"):
    """
    Creates a pipeline using the default /dev/video0 webcam when no device arg
    has been given in the v4l2src_args. A signal watch is added to the bus,
    calling on_message when a message arrives. Set state to playing, causing
    the data to be rendered.

    :param test_class: The class which uses the video player
    :param gst_elements: list of custom elements to be added to the pipeline
    :param v4l2src_args: string with arguments for the v4l2src element
    :param seperator: The seperator to use in the pipeline default "!"

    """
    Gst.init([])
    seperator = seperator.ljust(2).rjust(3)
    # Create pipeline string from elements
    elem_str = seperator.join(gst_elements)
    test_class.log.debug("Creating pipeline v4l2src " +
                         v4l2src_args + seperator + elem_str)
    test_class.video_player = Gst.parse_launch("v4l2src " + v4l2src_args + seperator + elem_str)

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
