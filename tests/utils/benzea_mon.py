from gi.repository import Gtk, Gdk, GLib

class Monitor(object):
    def __init__(self):
        pass
    @classmethod
    def from_monitor(cls, mon):
        res = cls()
        geometry = mon.get_geometry()
        res.height_mm = mon.get_height_mm()
        res.width_mm = mon.get_width_mm()
        res.manufacturer = mon.get_manufacturer()
        res.model = mon.get_model()
        res.scale = mon.get_scale_factor()
        res.app_x = geometry.x
        res.app_y = geometry.y
        res.app_width = geometry.width
        res.app_height = geometry.height
        # XXX: This is probably still wrong for 1.5 factor scaling!
        res.width = geometry.width * res.scale
        res.height = geometry.height * res.scale
        res.hash = hash(mon)
        return res
    @classmethod
    def from_screen(cls, screen, mon):
        res = cls()
        geometry = screen.get_monitor_geometry(mon)
        res.height_mm = screen.get_monitor_height_mm(mon)
        res.width_mm = screen.get_monitor_width_mm(mon)
        res.manufacturer = 'UNKNOWN'
        res.model = 'Plug: ' + screen.get_monitor_plug_name(mon)
        res.scale = screen.get_monitor_scale_factor(mon)
        res.app_x = geometry.x
        res.app_y = geometry.y
        res.app_width = geometry.width
        res.app_height = geometry.height
        # XXX: This is probably still wrong for 1.5 factor scaling!
        res.width = geometry.width * res.scale
        res.height = geometry.height * res.scale
        # Use the plug as a unique identifier
        res.hash = screen.get_monitor_plug_name(mon)
        return res
    def __repr__(self):
         return 'Monitor(%s, %s, %i, %i, scale=%i)' % (self.manufacturer, self.model, self.app_width, self.app_height, self.scale)
