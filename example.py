#!/usr/bin/env python

import os
from gi.repository import Gtk, Gdk, Pango, PangoCairo, Rsvg
import mapnik
from mapnik_pygi_widget.map_widget import MapWidget


def draw_track(width, height, cairo_context):
    global track_svg
    global svg_dimensions
    
    long_lat = mapnik.Coord(23.971774, 37.963283)
    x_y = map_widget.lon_lat_to_x_y(long_lat)
    
    cairo_context.save()
    cairo_context.translate(x_y.x-(svg_dimensions.width/2), x_y.y-(svg_dimensions.height/2))
    track_svg.render_cairo(cairo_context)
    cairo_context.restore()
    

track_svg = Rsvg.Handle.new_from_file("track.svg")
svg_dimensions = track_svg.get_dimensions()

win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)

map_widget = MapWidget(map_stylesheet="mapnik.xml", map_initial_bbox=mapnik.Envelope(20, 41, 28, 36), draw_cb=draw_track)


win.add(map_widget)

win.resize(800,600)

win.show_all()
Gtk.main()


