#  L_Menu.py. (Modified 2022-05-08, 3:45 p.m. by Praxis)
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
from .L_Menu_Text_Button import L_Menu_Text_Button
from .L_Menu_Special_Button import L_Menu_Special_Button

class L_Menu:
    ACTIVE_TAB = None  # Active tab in the main navigation menu
    ACTIVE_PANEL = None  # Active panel in an options menu
    def __init__(self, id: str, orientation: str, container_css_class: str, button_values: dict, button_css_class: str, content_manager: object, message_callback: classmethod, align_button_labels: str ="default"):
        """ Constructor """
        self.id = id
        self.message_callback = message_callback  # Dialog OK | CANCEL messages - Open the editor or quit the application
        self.button_action_callbacks = {}
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

        for id_key in button_values:  # id_key -> Menu_0; Menu_1; etc
            if button_values[id_key]["TYPE"] == "Text":
                self.__menu_buttons[id_key] = {"BUTTON_OBJECT": L_Menu_Text_Button(key=id_key, label=button_values[id_key]["LABEL"],
                                                                                   label_alignment=align_button_labels,
                                                                                   style_class=button_css_class,
                                                                                   callback=self.load_menu_request),
                                                "CONTENT_MANAGER": button_values[id_key]["CONTENT_MANAGER"]}
                if button_values[id_key]["ACTIVE"] is True:
                    self.track_active_menu(id_key)
                    self.__menu_buttons[id_key]["BUTTON_OBJECT"].set_style_name(self.__menu_button_css_active)
                    self.__load_tab_content(id_key)
                else:
                    self.__menu_buttons[id_key]["BUTTON_OBJECT"].set_style_name(self.__menu_button_css_inactive)
            elif button_values[id_key]["TYPE"] == "Special":
                self.__menu_buttons[id_key] = {"BUTTON_OBJECT": L_Menu_Special_Button(key=id_key,
                                                                                      label=button_values[id_key]["LABEL"],
                                                                                      style_class=button_values[id_key]["STYLE_CLASS"],
                                                                                      active_state=button_values[id_key]["ACTIVE"],
                                                                                      active_class=button_values[id_key]["ACTIVE_CLASS"],
                                                                                      tooltip=button_values[id_key]["TOOLTIP"],
                                                                                      callback=self.load_menu_request),
                                                "CONTENT_MANAGER": button_values[id_key]["CONTENT_MANAGER"]}

            if button_values[id_key]["PACK"] == "Start":
                self.__layout_container.pack_start(child=self.__menu_buttons[id_key]["BUTTON_OBJECT"].get_button(), expand=False, fill=False, padding=0)
            else:
                self.__layout_container.pack_end(child=self.__menu_buttons[id_key]["BUTTON_OBJECT"].get_button(), expand=False, fill=False, padding=0)


            if "ACTION_CALLBACK" in button_values[id_key]:
                self.button_action_callbacks[id_key] = button_values[id_key]["ACTION_CALLBACK"]


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

        if self.__active_tab_key == "MENU_3" and self.id == "main_menu":
            self.__active_tab_key = self.__class__.ACTIVE_TAB
        else:
            self.__active_tab_key = key

        self.__content_manager.add_layout_container(self.__menu_buttons[self.__active_tab_key]["CONTENT_MANAGER"].get_layout_container())

    def track_active_menu(self, key):
        # Register the current active tab in a class variable.
        if self.id == "main_menu":
            if key != "MENU_3":  # Exclude the 'help' menu tab ('Menu_3')
                self.__class__.ACTIVE_TAB = key
                panel_buttons = self.__menu_buttons[key]["CONTENT_MANAGER"].get_menu_buttons()
                if panel_buttons is None:
                    self.__class__.ACTIVE_PANEL = None
        else:
            self.__class__.ACTIVE_PANEL = key

    def help_button_clicked(self):
        self.load_menu_request("MENU_3")

    def load_menu_request(self, key) -> None:
        """ Public Processor: This function coordinates menu actions with the GUI_Manager. """
        self.track_active_menu(key)
        self.__activate_menu_button(key)
        self.__load_tab_content(key)
        self.message_callback(key)

        if key in self.button_action_callbacks:
            self.button_action_callbacks[key]()
