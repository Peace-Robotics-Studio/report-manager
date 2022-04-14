# L_Button.py
#
# Copyright 2022 Peace Robotics Studio

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class L_Button:
    def __init__(self, h_menu_layer, label, menu_number, style_class, style_name):
        """ Constructor
            h_menu_layer: handle to the L_Menu_Layer instance,
            label: label for the button,
            style_class: css style class,
            style_name: css name """
        self.__h_menu_layer = h_menu_layer
        self.__menu_number = menu_number
        # Create a button
        self.__button = Gtk.Button(label=label)
        self.__button.connect("clicked", self.button_clicked)
        self.__button.get_style_context().add_class(style_class)
        self.__button.set_name(style_name)
        self.__button.set_can_focus(False)

    def get_button(self) -> Gtk.Button:
        """ Public Accessor: This function returns Gtk.Button object used in the menu. """
        return self.__button

    def button_clicked(self, button):
        self.__h_menu_layer.process_menu_selection(self.__menu_number)

    def set_style_name(self, style_name):
        self.__button.set_name(style_name)
