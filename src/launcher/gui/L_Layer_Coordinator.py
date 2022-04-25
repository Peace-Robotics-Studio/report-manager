#  L_Layer_Coordinator.py. (Modified 2022-04-23, 8:30 p.m. by Praxis)
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
from .L_Banner_Layer import L_Banner_Layer
from .L_Menu_Layer import L_Menu_Layer
from .L_Content_Manager import L_Content_Manager
from ...Config import *


class L_Layer_Coordinator:
    def __init__(self, h_dialog: Gtk.Dialog, l_width: int, l_height: int, banner_height: int, menu_button_height: int):
        """ Constructor
            This class coordinates messages and actions between different layers of the interface.
            h_dialog: handle to the launcher dialog instance,
            l_width: width of the launcher window (int),
            l_height: height of the launcher window (int),
            banner_height: height of the clickable banner image (int),
            config_button_height: height of the button in the configuration menu.

            Definitions:
            category_menu = the menu providing a choice of task categories
            option_menu = a submenu having various options related to the task category
            action_panel = any interface elements causing a change in the state of the application window
            content_area = any container having visible elements or information shown to the user """
        self.__h_dialog = h_dialog  # Handle to the system Gtk.Dialog object window
        self.__launcher_properties = {  # Properties defining the dialog window and key sizes
            "WINDOW_HANDLE": h_dialog,
            "LAUNCHER_WIDTH": l_width,
            "LAUNCHER_HEIGHT": l_height,
            "BANNER_HEIGHT": banner_height,
            "MENU_BUTTON_HEIGHT": menu_button_height
        }
        # GUI initialization routines
        self.__interface_layer = Gtk.Overlay()
        self.__layer_order = {}
        self.__build_default_interface()

    def __build_default_interface(self):
        """ Private Task: This function instantiates layout manager objects for each layer and orders these objects based on their 'LAYER_ORDER' value """
        # Expected dictionary format: [layer manager, layer order, input passthrough]
        # Placing the CATEGORY_MENU in its own layer allows for drop-down lists that cover the content area
        self.__layer_order["BANNER"] = {"LAYER_ORDER": 1, "LAYER_OBJECT": L_Banner_Layer(launcher_properties=self.__launcher_properties, message_callback=self.process_action), "PASS_THROUGH": True}
        self.__layer_order["CONTENT"] = {"LAYER_ORDER": 0, "LAYER_OBJECT": L_Content_Manager(launcher_properties=self.__launcher_properties), "PASS_THROUGH": False}
        self.__layer_order["CATEGORY_MENU"] = {"LAYER_ORDER": 2, "LAYER_OBJECT": L_Menu_Layer(launcher_properties=self.__launcher_properties, content_manager=self.__layer_order["CONTENT"]["LAYER_OBJECT"], message_callback=self.process_action), "PASS_THROUGH": True}
        for i in range(len(self.__layer_order)):
            for key in self.__layer_order:
                if self.__layer_order[key]["LAYER_ORDER"] == i:
                    self.__add_display_layer(layout_container=self.__layer_order[key]["LAYER_OBJECT"].get_layout_container(), pass_through=self.__layer_order[key]["PASS_THROUGH"])

    def __add_display_layer(self, layout_container: Gtk.Container, pass_through=False):
        """ Private Task: Adds a layout container to the Gtk.Overlay widget and sets the pass_through flag. """
        # Gtk uses set_overlay_pass_through() for passing input events through to underlying overlay layers ->
        self.__interface_layer.add_overlay(layout_container)
        if pass_through is True:
            self.__interface_layer.set_overlay_pass_through(layout_container, True)

    def get_overlay(self):
        """ Public Accessor: This function returns a Gtk.Overlay object used for layering window content. """
        return self.__interface_layer

    def process_action(self, action: str, data=None):
        match action:
            case "quit" | "editor":
                self.__h_dialog.exit_launcher(action)
            case "load":
                self.__h_dialog.load_editor(action, data)

