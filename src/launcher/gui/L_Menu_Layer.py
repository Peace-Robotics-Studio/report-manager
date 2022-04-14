# L_Menu_Layer.py
#
# Copyright 2022 Peace Robotics Studio

import cairo
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk
from .L_Button import L_Button
from ...Settings import *

class L_Menu_Layer:

    def __init__(self, h_gui_manager, launcher_properties):
        """ Constructor
            h_gui_manager: Handle to GUI_Manager instance,
            launcher_properties: dictionary including width, height, banner_height """
        self.__h_gui_manager = h_gui_manager
        self.__launcher_properties = launcher_properties
        self.__menu_buttons = {}
        self.__layout_container = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        self.__build_layer()

    def get_layout_container(self) -> Gtk.Grid:
        """ Public Accessor: This function returns the Gtk layout container """
        return self.__layout_container

    def __build_layer(self) -> None:
        """ Private Initilizer: This function composes the menu layout """
        self.__menu_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__menu_area.get_style_context().add_class('content')
        self.__menu_area.set_hexpand(True)
        self.__menu_area.set_vexpand(True)
        self.__menu_area.set_margin_top(self.__launcher_properties['BANNER_HEIGHT'])
        self.__menu_area.set_margin_bottom(self.__launcher_properties['LAUNCHER_HEIGHT'] - self.__launcher_properties['BANNER_HEIGHT'] - self.__launcher_properties['CONFIG_BUTTON_HEIGHT'])
        self.__build_menu_buttons()

        self.__layout_container.attach(child=self.__menu_area, left=0, top=1, width=1, height=1)
        for index, button in enumerate(self.__menu_buttons, start=0):
            self.__menu_area.pack_start(child=self.__menu_buttons[button].get_button(), expand=False, fill=False, padding=0)

    def __build_menu_buttons(self) -> None:
        for i in range(len(configuration_menu_labels)):
            self.__menu_buttons[configuration_menu_labels[i]] = L_Button(self, configuration_menu_labels[i], 'button-background', 'green-button')

    def process_button_click(self, data):
        print(data)