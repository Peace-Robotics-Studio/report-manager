#  L_Banner_Layer.py. (Modified 2022-04-15, 6:56 p.m. by Praxis)
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
from ...Settings import *

class L_Banner_Layer:

    def __init__(self, h_gui_manager, launcher_properties):
        """ Constructor
            h_gui_manager: Handle to GUI_Manager instance,
            launcher_properties: dictionary including width, height, banner_height """
        self.__h_gui_manager = h_gui_manager
        self.__launcher_properties = launcher_properties
        self.__banner_container_css_class = 'launcher-banner-container'
        self.__banner_close_button_css_class = 'launcher-banner-close-button'
        self.__banner_close_button_css_name = 'close-button'
        self.__banner_build_number_css_class = 'launcher-banner-build-number'
        self.__layout_container = Gtk.Grid(column_spacing=0, row_spacing=0)
        self.__build_layer() # Initialization step

    # Private Methods

    def __build_layer(self) -> None:
        """ Private Initializer: This function composes the banner layout """
        banner_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__layout_container.attach(child=banner_area, left=0, top=0, width=1, height=1)
        banner_area.get_style_context().add_class(self.__banner_container_css_class)
        banner_area.set_hexpand(True)
        close_button = Gtk.Button()
        close_button.connect("clicked", self.close_button_clicked)
        close_button.get_style_context().add_class(self.__banner_close_button_css_class)
        close_button.set_name(self.__banner_close_button_css_name)
        banner_area.pack_end(child=close_button, expand=False, fill=False, padding=0)
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__layout_container.attach(child=box, left=0, top=1, width=1, height=1)
        box.get_style_context().add_class(self.__banner_build_number_css_class)  # Connect a CSS class to the label
        box.set_hexpand(True)
        box.set_vexpand(True)
        box.set_valign(Gtk.Align.END)
        # Set the bottom margin to (window_height - banner_height)
        box.set_margin_bottom(self.__launcher_properties['LAUNCHER_HEIGHT'] - self.__launcher_properties['BANNER_HEIGHT'])
        label = Gtk.Label()  # Add a label to the box
        box.pack_end(child=label, expand=False, fill=False, padding=0)
        label.set_text("v2022.04.15")  # Set the value of the label text
        # label.get_style_context().add_class('label-notification')  # Connect a CSS class to the label


    # Public Methods

    def get_layout_container(self) -> Gtk.Grid:
        """ Public Accessor: This function returns the Gtk layout container """
        return self.__layout_container

    def close_button_clicked(self, button) -> None:
        """ Public Processor: This function coordinates menu actions with the GUI_Manager. """
        self.__h_gui_manager.process_action("quit")

