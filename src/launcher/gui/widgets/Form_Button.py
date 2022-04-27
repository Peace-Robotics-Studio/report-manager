#  Form_Button.py. (Modified 2022-04-26, 7:37 p.m. by Praxis)
#  Copyright (c) 2022-2022 Peace Robotics Studio
#  Licensed under the MIT License.
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so.

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class Form_Button:
    """ Buttons used in forms (such as Tabular_Display()) """
    def __init__(self, callback: callable, name: str, active: bool = True, tooltip_text: str = None):
        self.is_active = active
        self.__name = name
        self.form_button = Gtk.Button()
        self.form_button.set_tooltip_text(tooltip_text)
        self.form_button.get_style_context().add_class('form-button')
        self.form_button.connect("clicked", callback, name)
        if active is True:
            self.form_button.get_style_context().add_class('active-item')
            self.form_button.set_name(name + "-active")
        else:
            self.form_button.get_style_context().add_class('inactive-item')
            self.form_button.set_name(name + "-inactive")

    def add(self):
        return self.form_button

    def set_active(self):
        if self.is_active is False:
            self.form_button.get_style_context().remove_class('inactive-item')
            self.form_button.get_style_context().add_class('active-item')
            self.form_button.set_name(self.__name + "-active")

    def set_inactive(self):
        if self.is_active is True:
            self.form_button.get_style_context().remove_class('active-item')
            self.form_button.get_style_context().add_class('inactive-item')
            self.form_button.set_name(self.__name + "-inactive")