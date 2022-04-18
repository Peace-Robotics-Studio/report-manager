#  L_Menu_Button.py. (Modified 2022-04-17, 3:26 p.m. by Praxis)
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
    def __init__(self, key: str, label: str, style_class: str, callback: classmethod, label_alignment: str ="default"):
        """ Constructor
            key: identification name of the button
            label: label for the button,
            style_class: css style class,
            callback:  """
        self.__key = key
        self.__callback = callback
        self.__button = Gtk.Button(label=label)
        match label_alignment:
            case "left" | "right":
                self.__button.get_child().set_xalign(0) if label_alignment == "left" else self.__button.get_child().set_xalign(1)
        self.__button.connect("clicked", self.button_clicked)
        self.__button.get_style_context().add_class(style_class)
        self.__button.set_can_focus(False)

    def get_button(self) -> Gtk.Button:
        """ Public Accessor: This function returns Gtk.Button object used in the menu. """
        return self.__button

    def button_clicked(self, button):
        self.__callback(self.__key)

    def set_style_name(self, style_name):
        self.__button.set_name(style_name)
