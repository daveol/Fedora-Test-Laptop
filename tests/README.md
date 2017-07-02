## Required packages per test subject

* wifi, ethernet tests:
    * libnm
    * GLib
* radio kill test:
    * libnm
    * GLib
    * rfkill
    * PyBluez
* bluetooth tests:
    * PyBluez
* webcam tests:
    * qrtools (https://github.com/primetang/qrtools), this tool also requires
    pillow, zbar and pypng. The GitHub version works while the package from pip
    does not.
    * Gtk
    * Gst
* display tests:
    * gnome
