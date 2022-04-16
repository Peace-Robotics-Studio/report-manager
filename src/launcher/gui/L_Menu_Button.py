#  L_Menu_Button.py. (Modified 2022-04-15, 3:03 p.m. by Praxis)
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

class L_Menu_Button:
    def __init__(self, h_menu_layer: object, label: str, menu_key: str, style_class: str, style_name: str):
        """ Constructor
            h_menu_layer: handle to the L_Menu_Layer instance,
            label: label for the button,
            style_class: css style class,
            style_name: css name """
        self.__h_menu_layer = h_menu_layer
        self.__menu_key = menu_key
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
        self.__h_menu_layer.process_menu_selection(self.__menu_key)

    def set_style_name(self, style_name):
        self.__button.set_name(style_name)
