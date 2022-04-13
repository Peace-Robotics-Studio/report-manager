# Launcher_Interface.py
#
# Copyright 2022 Peace Robotics Studio

import gi
import sys
import cairo

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from src.Settings import res_dir
from .gui.L_GUI_Manager import L_GUI_Manager

class Report_Manager_Launcher(Gtk.Dialog):
    def __init__(self, parent):
        """ Constructor """
        Gtk.Dialog.__init__(self)   # Initialize Gtk.Dialog super class
        # Set the name for the image used to define the launcher hit area
        self.__launcher_properties = dict(
            BANNER=cairo.ImageSurface.create_from_png(res_dir['GUI'] + 'window-image.png'),
            BANNER_HEIGHT=191   # This is the part of the image users will click on to move the window
        )
        self.__launcher_properties['WIDTH'] = self.__launcher_properties['BANNER'].get_width()      # Width of window image
        self.__launcher_properties['HEIGHT'] = self.__launcher_properties['BANNER'].get_height()    # Height of window image
        self.__gui_manager = L_GUI_Manager(l_width=self.__launcher_properties['WIDTH'], l_height=self.__launcher_properties['HEIGHT'], banner_height=self.__launcher_properties['BANNER_HEIGHT'])

        # Create a window with the same dimensions as the image
        self.set_default_size(self.__launcher_properties['WIDTH'], self.__launcher_properties['HEIGHT'])
        self.set_decorated(False)  # Creates a borderless window without a title bar
        self.set_app_paintable(True)
        self.connect('draw', self.draw)    # Capture signal and set callback
        self.connect("button-press-event", self.do_button_press_event)  # Capture signal and set callback
        self.connect("motion-notify-event", self.do_button_movement)    # Capture signal and set callback

        # Obtain handle to the drawable area of the dialog window and attach a container to manage content
        area = self.get_content_area()
        # Adds a drawing layer to the dialog window
        area.add(self.__gui_manager.get_overlay())
        self.show_all()

    def do_button_press_event(self, widget, event) -> bool:
        """ Callback function triggered by the button-press-event signal. """
        # Check to make sure the left mouse button was clicked
        if event.button == Gdk.BUTTON_PRIMARY:
            self.window_x, self.window_y = self.get_position()
            self.mouse_x = event.x_root
            self.mouse_y = event.y_root
        return True  # Returning true prevents the event from being propagated to other event handlers

    def do_button_movement(self, widget, event) -> None:
        """ Callback function triggered by the motion-notify-event signal. """
        state = event.get_state()
        # Check to see if it was the left mouse button that was clicked
        if state & Gdk.ModifierType.BUTTON1_MASK:
            # Only move the window if the 'click' happened in the dialog banner
            if event.y_root < self.window_y + self.__launcher_properties['BANNER_HEIGHT']:
                # Calculate the difference between the current mouse location and the previous mouse location
                delta_x = self.mouse_x - event.x_root
                delta_y = self.mouse_y - event.y_root
                # Modify the location of the window along x,y by deltas calculated above
                self.window_x -= delta_x
                self.window_y -= delta_y
                self.move(self.window_x, self.window_y)
                # Store current mouse coordinates for reference
                self.mouse_x = event.x_root
                self.mouse_y = event.y_root

    def draw(self, widget, context) -> None:
        """ Callback function triggered by the draw signal.
         Gtk.Widget.input_shape_combine_region() uses an X server extension on the X11 platform and does not work on other platforms. """
        input_region = Gdk.cairo_region_create_from_surface(self.__launcher_properties['BANNER'])
        self.input_shape_combine_region(input_region)
        context.set_operator(cairo.OPERATOR_SOURCE)
        context.set_source_surface(self.__launcher_properties['BANNER'], 0, 0)
        context.paint()
        context.set_operator(cairo.OPERATOR_OVER)

