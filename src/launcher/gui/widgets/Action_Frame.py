#  Action_Frame.py. (Modified 2022-05-27, 10:45 p.m. by Praxis)
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
from .Frame_Button import Frame_Button
from abc import ABC


class Action_Frame(ABC):
    def __init__(self, css_class: str = "table-list-container", css_name: str = None):
        """ Constructor """
        super().__init__()
        self.TOGGLE_BUTTONS = {}
        self.BUTTON_CALLBACKS = {}
        self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.__layout_container.set_vexpand(True)
        self.__layout_container.get_style_context().add_class(css_class)
        if css_name is not None:
            self.__layout_container.set_name(css_name)
        self.__action_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__action_bar.get_style_context().add_class('action-bar')

        self.__action_bar.set_hexpand(True)
        self.__layout_container.add(self.__action_bar)

        self.__action_bar_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__action_bar.pack_start(child=self.__action_bar_buttons, expand=False, fill=False, padding=0)

        self.__action_bar_buttons_start = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__action_bar_buttons.pack_start(child=self.__action_bar_buttons_start, expand=False, fill=False, padding=0)

        self.__action_bar_buttons_center = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__action_bar_buttons.pack_start(child=self.__action_bar_buttons_center, expand=False, fill=False, padding=0)

        self.__action_bar_buttons_end = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__action_bar_buttons.pack_start(child=self.__action_bar_buttons_end, expand=False, fill=False, padding=0)

        self.list_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.list_container.get_style_context().add_class('table-list-data')
        self.__layout_container.add(self.list_container)
        self.list_container.set_hexpand(True)
        self.list_container.set_vexpand(True)

    def show_all(self):
        self.__layout_container.show_all()

    def display_data(self, widget: Gtk.Container, pack: str = "start", expand: bool = False, fill: bool = True, padding: int = 0):
        if pack == "end":
            self.list_container.pack_end(child=widget, expand=expand, fill=fill, padding=padding)
        else:
            self.list_container.pack_start(child=widget, expand=expand, fill=fill, padding=padding)

    def get_layout_container(self) -> Gtk.Container:
        """ Public Accessor: Returns Gtk.Container object. """
        return self.__layout_container

    def add_to_action_bar(self, item: Gtk.Widget, pack: str = "start", expand: bool = False, fill: bool = False, padding: int = 0):
        if pack == "end":
            self.__action_bar.pack_end(child=item, expand=expand, fill=fill, padding=padding)
        else:
            self.__action_bar.pack_start(child=item, expand=expand, fill=fill, padding=padding)

    def register_button(self, name: str, id: str, callback: callable, tooltip: str, interaction_type: str = "Button", group_key: str = "", active: bool = True, pack_order: str = "CENTER", has_context_menu: bool = False) -> Frame_Button:
        if id not in self.BUTTON_CALLBACKS:
            button = Frame_Button(name=name, id=id, callback=self.button_clicked_intercept, tooltip_text=tooltip, active=active, has_context_menu=has_context_menu)
            self.BUTTON_CALLBACKS[id] = callback
            if pack_order == "END":
                self.__action_bar_buttons_end.add(button)
            elif pack_order == "CENTER":
                self.__action_bar_buttons_center.add(button)
            else:
                self.__action_bar_buttons_start.add(button)
            if interaction_type == "toggle":
                self.TOGGLE_BUTTONS[id] = {"status": active, "object": button, "group_key": group_key}
            return button
        else:
            print('\033[3;30;43m' + ' Error! Attempt to register a duplicate button ID ' + '\033[0m')

    def button_clicked_intercept(self, button, id):
        if id in self.TOGGLE_BUTTONS:
            self.toggle_button_clicked(id)
        self.BUTTON_CALLBACKS[id](button, id)

    def toggle_button(self, id):
        if self.TOGGLE_BUTTONS[id]["status"]:  # Button is active
            self.TOGGLE_BUTTONS[id]["object"].set_inactive()  # Set this button as inactive
            self.TOGGLE_BUTTONS[id]["status"] = False  # Set its active status to False
            for button_name, properties in self.TOGGLE_BUTTONS.items():  # Loop through all registered buttons
                if properties["group_key"] == self.TOGGLE_BUTTONS[id]["group_key"]:  # Find buttons with matching group keys
                    if button_name != id:  # Exclude this button from the matches
                        self.toggle_button(button_name)
        else:
            self.TOGGLE_BUTTONS[id]["object"].set_active()
            self.TOGGLE_BUTTONS[id]["status"] = True

    def toggle_button_clicked(self, id):
        if self.TOGGLE_BUTTONS[id]["status"]:
            self.toggle_button(id)
