#  L_GUI_Manager.py. (Modified 2022-04-16, 1:28 p.m. by godvalve)
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
from .L_Content_Layer import L_Content_Layer
from ..tabs.L_Setup import L_Setup
from ..tabs.L_Reports import L_Reports
from ..tabs.L_Feedback import L_Feedback
from ...Settings import *


class L_GUI_Manager:
    def __init__(self, h_dialog: Gtk.Dialog, l_width: int, l_height: int, banner_height: int, menu_button_height: int):
        """ Constructor
            h_dialog: handle to the launcher dialog instance,
            l_width: width of the launcher window (int),
            l_height: height of the launcher window (int),
            banner_height: height of the clickable banner image (int),
            config_button_height: height of the button in the configuration menu. """
        self.__h_dialog = h_dialog
        self.__launcher_properties = {
            "LAUNCHER_WIDTH": l_width,
            "LAUNCHER_HEIGHT": l_height,
            "BANNER_HEIGHT": banner_height,
            "MENU_BUTTON_HEIGHT": menu_button_height
        }
        self.__menu_tabs = dict(
            MENU_1=L_Setup(),
            MENU_2=L_Reports(),
            MENU_3=L_Feedback()
        )
        self.__interface_layer = Gtk.Overlay()
        # Stacking order of overlay layers
        self.__layer_order = dict(
            BANNER=0,
            MENU=1,
            CONTENT=2
        )
        self.__layer_objects = []
        self.__active_tab_key = None
        self.__build_default_interface()

    def __build_default_interface(self):
        """ Private Task: Composes layout of main gui. """
        # Expected dictionary format: [layer instance, layer order, input passthrough]
        self.__layer_objects.append([L_Banner_Layer(h_gui_manager=self, launcher_properties=self.__launcher_properties), self.__layer_order['BANNER'], False])
        self.__layer_objects.append([L_Menu_Layer(h_gui_manager=self, launcher_properties=self.__launcher_properties), self.__layer_order['MENU'], True])
        self.__layer_objects.append([L_Content_Layer(h_gui_manager=self, launcher_properties=self.__launcher_properties), self.__layer_order['CONTENT'], True])
        self.__add_overlays()
        self.load_content_area(default_launcher_menu_tab)

    def __add_overlays(self):
        """ Private Task: Iterates over a list of widgets and adds them to a Gtk.Overlay widget. """
        for layer in self.__layer_objects:
            self.__add_display_layer(layout_container=layer[0].get_layout_container(), pass_through=layer[2])

    def __add_display_layer(self, layout_container: Gtk.Container, pass_through=False):
        """ Private Task: Adds a layout container to the Gtk.Overlay widget and sets the pass_through flag. """
        # Gtk uses set_overlay_pass_through() for passing input events through to underlying overlay layers ->
        self.__interface_layer.add_overlay(layout_container)
        if pass_through is True:
            self.__interface_layer.set_overlay_pass_through(layout_container, True)

    def get_overlay(self):
        """ Public Accessor: This function returns a Gtk.Overlay object used for layering window content. """
        return self.__interface_layer

    def load_content_area(self, menu_key: str, sub_menu_label: str = None):
        """ Public Task: Swaps out layout containers in the content layer based on the key of the active menu. """
        if self.__active_tab_key is not None:
            self.__layer_objects[self.__layer_order['CONTENT']][0].remove_layout_container(self.__menu_tabs[self.__active_tab_key].get_layout_container())
        self.__active_tab_key = menu_key
        self.__layer_objects[self.__layer_order['CONTENT']][0].add_layout_container(self.__menu_tabs[menu_key].get_layout_container())

    def process_action(self, action: str, data=None):
        match action:
            case "quit":
                self.__h_dialog.exit_launcher(action)
            case "editor":
                self.__h_dialog.start_editor(action)
            case "load":
                self.__h_dialog.load_editor(action, data)

