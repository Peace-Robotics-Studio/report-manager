#  L_Menu_Special_Button.py. (Modified 2022-05-15, 9:48 p.m. by Praxis)
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

class L_Menu_Special_Button:
    def __init__(self, key: str, callback: classmethod, label: str = None, style_class: str = None, active_state: bool = True,
                 tooltip: str = None, active_class: str = None, inactive_class: str = None, label_alignment: str = "left"):
        """ Constructor
            key: identification name of the button
            label: label for the button,
            style_class: css style class,
            callback:  """
        self.__key = key
        self.__active_state = active_state
        self.__active_class = active_class
        self.__inactive_class = inactive_class
        self.__callback = callback
        self.__button = Gtk.Button()
        if label:
            self.__button.set_label(label)
            match label_alignment:
                case "left" | "right":
                    self.__button.get_child().set_xalign(0) if label_alignment == "left" else self.__button.get_child().set_xalign(1)
        if tooltip is not None:
            self.__button.set_tooltip_text(tooltip)  # This doesn't appear to work. Bug with Gtk.Overlay with pass_through set to True
        self.__button.connect("clicked", self.button_clicked)
        self.__button.get_style_context().add_class(style_class)
        self.set_active_state(active_state)
        self.__button.set_can_focus(False)

    def get_button(self) -> Gtk.Button:
        """ Public Accessor: This function returns Gtk.Button object used in the menu. """
        return self.__button

    def set_active_state(self, is_active: bool):
        """ Public Task: Set the CSS state for active or inactive button """
        self.__active_state = is_active
        if is_active:
            if self.__active_class is not None:
                if self.__inactive_class is not None:
                    self.__button.get_style_context().remove_class(self.__inactive_class)
                self.__button.get_style_context().add_class(self.__active_class)
        else:
            if self.__inactive_class is not None:
                if self.__active_class is not None:
                    self.__button.get_style_context().remove_class(self.__active_class)
                self.__button.get_style_context().add_class(self.__inactive_class)

    def button_clicked(self, button):
        """ Callback: Triggered by button click """
        self.__callback(self.__key)

    def set_style_name(self, style_name):
        """ Set the CSS name """
        self.__button.set_name(style_name)
