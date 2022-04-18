#  L_Menu.py. (Modified 2022-04-17, 3:52 p.m. by Praxis)
#  Copyright (c) 2022-2022 Peace Robotics Studio
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
from .L_Menu_Button import L_Menu_Button

class L_Menu:
    def __init__(self, orientation: str, container_css_class: str, button_values: dict, button_css_class: str, content_manager: object, message_callback: classmethod, align_button_labels: str ="default"):
        """ Constructor """
        self.message_callback = message_callback
        self.__content_manager = content_manager
        if orientation.lower() == "horizontal":
            self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            self.__layout_container.set_hexpand(True)
        else:
            self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            self.__layout_container.set_vexpand(True)
        self.__layout_container.get_style_context().add_class(container_css_class)
        self.__menu_button_css_active = 'active-menu-button'
        self.__menu_button_css_inactive = 'inactive-menu-button'
        self.__menu_buttons = {}
        self.__active_tab_key = None
        for key in button_values:
            self.__menu_buttons[key] = {"BUTTON_OBJECT": L_Menu_Button(key=key, label=button_values[key]["LABEL"], label_alignment=align_button_labels, style_class=button_css_class, callback=self.load_menu_request),
                                        "CONTENT_MANAGER": button_values[key]["CONTENT_MANAGER"]}
            if button_values[key]["ACTIVE"] is True:
                self.__menu_buttons[key]["BUTTON_OBJECT"].set_style_name(self.__menu_button_css_active)
                self.__load_tab_content(key)
            else:
                self.__menu_buttons[key]["BUTTON_OBJECT"].set_style_name(self.__menu_button_css_inactive)
            self.__layout_container.pack_start(child=self.__menu_buttons[key]["BUTTON_OBJECT"].get_button(), expand=False, fill=False, padding=0)

    def get_layout_container(self):
        """ Public Accessor: This function returns the Gtk layout container """
        return self.__layout_container

    def __activate_menu_button(self, key: str):
        """ Private Initializer: This function modifies CSS style attributes for active and inactive menu buttons. """
        if self.__active_tab_key != key:
            self.__menu_buttons[key]["BUTTON_OBJECT"].set_style_name(self.__menu_button_css_active)
            self.__menu_buttons[self.__active_tab_key]["BUTTON_OBJECT"].set_style_name(self.__menu_button_css_inactive)

    def __load_tab_content(self, key: str, sub_menu_label: str = None):
        """ Private Task: Swaps out layout containers in the content layer based on the key of the active menu. """
        if self.__active_tab_key is not None:
            self.__content_manager.remove_layout_container(self.__menu_buttons[self.__active_tab_key]["CONTENT_MANAGER"].get_layout_container())
        self.__active_tab_key = key
        self.__content_manager.add_layout_container(self.__menu_buttons[key]["CONTENT_MANAGER"].get_layout_container())

    def load_menu_request(self, key) -> None:
        """ Public Processor: This function coordinates menu actions with the GUI_Manager. """
        self.__activate_menu_button(key)
        self.__load_tab_content(key)
        self.message_callback(key)
