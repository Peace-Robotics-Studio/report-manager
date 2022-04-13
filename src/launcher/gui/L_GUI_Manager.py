# L_GUI_Manager.py
#
# Copyright 2022 Peace Robotics Studio

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .L_Menu_Layer import L_Menu_Layer

class L_GUI_Manager:
    def __init__(self, l_width, l_height, banner_height):
        """ Constructor
        l_width: width of the launcher window (int)
        l_height: height of the launcher window (int)
        banner_height: height of the clickable banner image (int)"""
        self.__launcher_properties = {
          "WIDTH": l_width,
          "HEIGHT": l_height,
          "BANNER_HEIGHT": banner_height
        }
        self.__interface_layer = Gtk.Overlay()
        self.__layers = []
        self.__build_default_interface()

    def __build_default_interface(self):
        """ Private Task: composes layout of main gui. """
        # Expected dictionary format: [layer instance, layer order, input passthrough]
        self.__layers.append([L_Menu_Layer(launcher_properties=self.__launcher_properties), 0, False])
        self.__add_overlays()

    def __add_overlays(self):
        """ Private Task: Iterates over a list of widgets and adds them to a Gtk.Overlay widget. """
        for layer in self.__layers:
            self.__add_display_layer(layout_container=layer[0].get_layout_container(), pass_through=layer[2])

    def __add_display_layer(self, layout_container, pass_through=False):
        """ Private Task: Adds a layout container to the Gtk.Overlay widget and sets the pass_through flag. """
        # Gtk uses set_overlay_pass_through() for passing input events through to underlying overlay layers ->
        self.__interface_layer.add_overlay(layout_container)
        if pass_through is True:
            self.__interface_layer.set_overlay_pass_through(layout_container, True)

    def get_overlay(self):
        """ Public Accessor: This function returns Gtk.Overlay object used for layering window content. """
        return self.__interface_layer

    def load_content_area(self, menu_label: str, sub_menu_label: str = None):
        """ Public Task: Swaps out layout containers in the main content layer based on the value of the active
        menu. The value of the menu_label parameter is taken from the label of the menu button that was pressed. """
