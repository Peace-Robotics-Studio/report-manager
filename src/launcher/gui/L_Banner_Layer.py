#  L_Banner_Layer.py. (Modified 2022-04-17, 12:14 p.m. by Praxis)
#  Copyright (c) 2021-2022 Peace Robotics Studio
#  Licensed under the MIT License.
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so.

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from .ABS_Content_Layer import Content_Layer
from ...Config import *

class L_Banner_Layer(Content_Layer):

    def __init__(self, launcher_properties, message_callback):
        """ Constructor: Inherits from Content_Layer abstract class
            h_gui_manager: Handle to GUI_Manager instance,
            launcher_properties: dictionary including width, height, banner_height """
        super().__init__()
        self.__launcher_properties = launcher_properties
        self.__message_callback = message_callback
        self.__banner_container_css_class = 'launcher-banner-container'
        self.__banner_close_button_css_class = 'launcher-banner-close-button'
        self.__banner_close_button_css_name = 'close-button'
        self.__banner_build_number_css_class = 'launcher-banner-build-number'
        # self.__layout_container = Gtk.Grid(column_spacing=0, row_spacing=0)
        self.__build_layer() # Initialization step

    # Private Methods

    def __build_layer(self) -> None:
        """ Private Initializer: This function composes the banner layout """
        # Create a box to hold the close button
        banner_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        super().attach_to_grid(child=banner_area, left=0, top=0, width=1, height=1)
        banner_area.get_style_context().add_class(self.__banner_container_css_class)
        banner_area.set_hexpand(True)
        # Add the close button
        close_button = Gtk.Button()
        close_button.set_can_focus(False)
        close_button.connect("clicked", self.close_button_clicked)
        close_button.get_style_context().add_class(self.__banner_close_button_css_class)
        close_button.set_name(self.__banner_close_button_css_name)
        banner_area.pack_end(child=close_button, expand=False, fill=False, padding=0)
        # Create a box to hold the build number label
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        super().attach_to_grid(child=box, left=0, top=1, width=1, height=1)
        box.get_style_context().add_class(self.__banner_build_number_css_class)  # Connect a CSS class to the label
        box.set_hexpand(True)
        box.set_vexpand(True)
        box.set_valign(Gtk.Align.END)
        box.set_margin_bottom(self.__launcher_properties['LAUNCHER_HEIGHT'] - self.__launcher_properties['BANNER_HEIGHT']) # Set the bottom margin to (window_height - banner_height)
        label = Gtk.Label()  # Add a label to the box
        # Add the label
        box.pack_end(child=label, expand=False, fill=False, padding=0)
        label.set_text(version_number)  # Set the value of the label text

    # Public Methods

    def close_button_clicked(self, button) -> None:
        """ Public Processor: This function coordinates menu actions with the GUI_Manager. """
        self.__message_callback("quit")

