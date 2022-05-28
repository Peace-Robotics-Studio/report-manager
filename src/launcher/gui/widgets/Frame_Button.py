#  Frame_Button.py. (Modified 2022-05-27, 10:50 p.m. by Praxis)
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
from gi.repository import Gtk
from .Context_Menu_Dialog import Context_Menu_Dialog
from .Context_Menu_Item import Context_Menu_Item_Properties


class Frame_Button(Gtk.Button):
    """ Buttons used in forms (such as Tabular_Display()) """
    def __init__(self, callback: callable, name: str, id: str, active: bool = True, tooltip_text: str = None, has_context_menu: bool = False):
        super().__init__()
        self.is_active = active
        self.__name = name
        self.__context_menu_items = []
        self.__has_context_menu = has_context_menu
        self.__context_menu_alignment = "right"
        # self.form_button = Gtk.Button()
        self.set_tooltip_text(tooltip_text)
        self.get_style_context().add_class('form-button')
        if not has_context_menu:
            self.connect("clicked", callback, id)
        else:
            self.connect("clicked", self.__display_context_menu)
        if active is True:
            self.get_style_context().add_class('active-item')
            self.set_name(name + "-active")
        else:
            self.get_style_context().add_class('inactive-item')
            self.set_name(name + "-inactive")

    def set_active(self):
        if self.is_active is False:
            self.get_style_context().remove_class('inactive-item')
            self.get_style_context().add_class('active-item')
            self.set_name(self.__name + "-active")
            self.is_active = True

    def set_inactive(self):
        if self.is_active is True:
            self.get_style_context().remove_class('active-item')
            self.get_style_context().add_class('inactive-item')
            self.set_name(self.__name + "-inactive")
            self.is_active = False

    def set_context_menu_left(self):
        self.__context_menu_alignment = "left"

    def set_context_menu_right(self):
        self.__context_menu_alignment = "right"

    def __display_context_menu(self, button):
        """ Private Callback: This function creates a context menu when the settings button is activated. """
        context_dialog = Context_Menu_Dialog(parent=self.get_toplevel(), reference_widget=button, align=self.__context_menu_alignment, form_items=self.__context_menu_items)
        response = context_dialog.run()
        # if response == Gtk.ResponseType.OK:
        #     print("The OK button was clicked")
        context_dialog.destroy()

    def add_context_menu_item(self, label: str, response_key: str, callback: callable, active: bool = True, toggled_on: bool = False, decorator: str = None, title: bool = False, menu: bool = False):
        self.__context_menu_items.append(Context_Menu_Item_Properties(label=label,
                                                                      response_key=response_key,
                                                                      callback=callback,
                                                                      active=active,
                                                                      toggled_on=toggled_on,
                                                                      decorator=decorator,
                                                                      title=title,
                                                                      menu=menu))
