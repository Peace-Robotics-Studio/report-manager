#  Context_Box.py. (Modified 2022-04-24, 8:25 p.m. by Praxis)
#  Copyright (c) 2022-2022 Peace Robotics Studio
#  Licensed under the MIT License.
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so.

import gi
import cairo

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from .Form_Item import Form_Item
from ....Config import *


class Context_Box(Gtk.Dialog):
    def __init__(self, parent, reference_widget: Gtk.Widget, align: str, form_items: list):
        """ Constructor:  """
        super().__init__(flags=0)
        # Set properties for the dialog window
        self.set_default_size(100, 25)
        self.set_border_width(0)
        self.__form_items = form_items
        self.__parent_window = parent
        self.__reference_widget = reference_widget
        self.__alignment = align
        self.set_decorated(False)  # Remove the window border
        self.add_events(Gdk.EventMask.FOCUS_CHANGE_MASK)
        self.connect("focus-out-event", self.__window_focus_lost)
        self.set_app_paintable(True)
        self.connect('draw', self.__create_background)
        # Create a container to hold content for this dialog window.
        window_area = self.get_content_area()
        self.layout_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.layout_container.get_style_context().add_class('context-box-container')  # Use CSS to set new background colour
        self.layout_container.set_hexpand(True)
        self.layout_container.set_vexpand(True)
        window_area.add(self.layout_container)
        # Make the dialog box visible
        self.build_form_items()
        self.show_all()
        # Move the box (based on its final dimensions) to a position under the reference widget
        self.__adjust_window_size()

    def __adjust_window_size(self):
        alloc = self.get_allocation()
        self.__window_width = alloc.width
        self.window_x, self.window_y = self.__get_position()
        self.move(self.window_x, self.window_y)

    def __get_position(self):
        """ Private Task: Calculates the window location coordinates of the dialog relative to a reference widget. """
        win_x, win_y = self.__parent_window.get_position()  # Get the origin coordinates of the parent window
        target_widget_allocation = self.__reference_widget.get_allocation()  # Get the relative coordinates and dimensions of the reference widget
        x = target_widget_allocation.x
        y = target_widget_allocation.y
        # Calculate the new top-left coordinate values for the dialog window
        if self.__alignment == "left":
            # Align the top-left of the dialog to the bottom-left of the reference widget
            absolute_x = win_x + x
            absolute_y = win_y + y + target_widget_allocation.height
        else:
            # Align the top-right of the dialog to the bottom-right of the reference widget
            absolute_x = win_x + x - self.__window_width + target_widget_allocation.width + 3
            absolute_y = win_y + y + target_widget_allocation.height
        return absolute_x, absolute_y

    def __window_focus_lost(self, widget, event):
        """ Private Task: Detects that the dialog window has lost focus and sends a close response. """
        self.response(Gtk.ResponseType.OK)

    def __create_background(self, widget, context):
        """ Private Initializer: Create a bespoke background surface for the dialog window. """
        # Get the size of the dialog window
        size = widget.get_allocation()
        width = size.width
        height = size.height
        # Create a surface to use as the background for this widget
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)
        # Clear the surface buffer
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.0)  # Transparent because the background shows up as a border for the window
        ctx.rectangle(0, 0, width, height)  # Draw a square outline with the same dimensions as the widget
        ctx.fill()  # Fill the outline with colour
        context.set_operator(cairo.OPERATOR_SOURCE)
        context.set_source_surface(surface, 0, 0)
        context.paint()
        context.set_operator(cairo.OPERATOR_OVER)

    def build_form_items(self):
        """ Public Initializer: This function adds form items to the context menu """
        if self.__form_items:
            for item_property_dictionary in self.__form_items:
                form_item = Form_Item(item_property_dictionary)
                self.layout_container.add(form_item.get_layout_container())
