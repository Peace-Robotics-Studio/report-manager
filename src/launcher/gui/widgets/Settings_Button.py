#  Settings_Button.py. (Modified 2022-05-27, 11:01 p.m. by Praxis)
#  Copyright (c) 2022 Peace Robotics Studio
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
from .Context_Menu_Dialog import Context_Menu_Dialog
from .Context_Menu_Item import Context_Menu_Item_Properties


class Settings_Button(Gtk.Button):
    def __init__(self, css_class: str, css_name: str, parent_window: Gtk.Window, label: str = None):
        super().__init__()
        self.__parent_window = parent_window
        self.__menu_items = []
        if label is not None:
            self.set_label(label=label)
        self.get_style_context().add_class(css_class)
        self.set_name(css_name)
        self.connect("clicked", self.__picker_config_context)

    def add_menu_item(self, label: str, response_key: str, callback: callable, active: bool = True, toggled_on: bool = False, decorator: str = None, title: bool = False, menu: bool = False):
        self.__menu_items.append(Context_Menu_Item_Properties(label=label, response_key=response_key, callback=callback, active=active, toggled_on=toggled_on, decorator=decorator, title=title, menu=menu))

    def __picker_config_context(self, button):
        """ Private Callback: This function creates a context menu when the picker config button is activated. """
        config_context = Context_Menu_Dialog(parent=self.__parent_window, reference_widget=button, align="right", form_items=self.__menu_items)
        response = config_context.run()
        # if response == Gtk.ResponseType.OK:
        #     print("The OK button was clicked")
        config_context.destroy()