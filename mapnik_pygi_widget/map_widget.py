#!/usr/bin/env python

'''
The MIT License (MIT)

Copyright (c) 2014 Georgios Migdos  <cyberpython@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from gi.repository import Gtk, Gdk, Pango, PangoCairo, Rsvg
import cairo
import mapnik

class MapWidget(Gtk.DrawingArea):
    def __init__ (self, upper=9, text='', map_stylesheet='', map_initial_bbox=None, draw_cb=None):
        Gtk.DrawingArea.__init__(self)
        self.__create_map(map_stylesheet, map_initial_bbox)
        self.__mouse_down = False
        self.__x0 = 0
        self.__y0 = 0
        self.__draw_cb = draw_cb
        self.__setup_signal_handling()
        
    def repaint(self):
        w = self.get_allocated_width()
        h = self.get_allocated_height()
        self.queue_draw_area(0,0,w,h)
    
    def lon_lat_to_x_y(self, long_lat):
        return self.__map.view_transform().forward(long_lat)
        
    def __create_map(self, stylesheet, initial_bbox):
        w = self.get_allocated_width()
        h = self.get_allocated_height()
        self.__map = mapnik.Map(w,h)
        mapnik.load_map(self.__map, stylesheet)
        
        if initial_bbox == None:
            self.__map.zoom_all()
        else:
            self.__map.zoom_to_box(initial_bbox)
            
    def __setup_signal_handling(self):
        self.set_events(self.get_events() + Gdk.EventMask.SCROLL_MASK + Gdk.EventMask.POINTER_MOTION_MASK + Gdk.EventMask.BUTTON_PRESS_MASK + Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.connect('draw', self.__do_draw_cb)
        self.connect('scroll-event', self.__do_zoom)
        self.connect('motion-notify-event', self.__do_pan)
        self.connect('button-press-event', self.__btn_pressed)
        self.connect('button-release-event', self.__btn_released)

    def __do_draw_cb(self, widget, cr0):
        cr = widget.get_window().cairo_create()
        cr.save()
        surface = cr.get_target()
        w = self.get_allocated_width()
        h = self.get_allocated_height()
        self.__map.resize(w, h)
        mapnik.render(self.__map, surface)
        if self.__draw_cb != None:
            self.__draw_cb(w, h, cr)
        surface.finish()
        cr.restore()
        return True
    
    def __do_zoom(self, widget, event):
        if event.direction == Gdk.ScrollDirection.UP:
            self.__map.zoom(0.9)
        elif event.direction == Gdk.ScrollDirection.DOWN:
            self.__map.zoom(1.1)
        self.queue_draw()
        return True
        
    def __btn_pressed(self, widget, event):
    
        self.__mouse_down = True
        self.__x0 = event.x
        self.__y0 = event.y
    
    def __btn_released(self, widget, event):
    
        self.__mouse_down = False
        self.__x0 = 0
        self.__y0 = 0
        
    def __do_pan(self, widget, event):
        if self.__mouse_down:
            dx = event.x - self.__x0
            dy = event.y - self.__y0
            self.__x0 = event.x
            self.__y0 = event.y
            if dx != 0 or dy != 0:        
                w = self.get_allocated_width()
                h = self.get_allocated_height()
                self.__map.pan(int(w/2 - dx), int(h/2 - dy))
                self.queue_draw()
                
                

          

