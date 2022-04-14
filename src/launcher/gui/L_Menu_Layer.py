# L_Menu_Layer.py
#
# Copyright 2022 Peace Robotics Studio

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
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
        if default_launcher_configuration_menu < len(launcher_configuration_menu_labels):
            self.__active_menu = default_launcher_configuration_menu
        else:
            self.__active_menu = 0
        self.__menu_button_css_class = 'launcher-menu'
        self.__menu_button_css_active = 'active-configure-button'
        self.__menu_button_css_inactive = 'inactive-configure-button'
        self.__layout_container = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        self.__build_layer()

    def get_layout_container(self) -> Gtk.Grid:
        """ Public Accessor: This function returns the Gtk layout container """
        return self.__layout_container

    def __build_layer(self) -> None:
        """ Private Initializer: This function composes the menu layout """
        self.__menu_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__menu_area.get_style_context().add_class('content')
        self.__menu_area.set_hexpand(True)
        self.__menu_area.set_vexpand(True)
        self.__menu_area.set_margin_top(
            self.__launcher_properties['BANNER_HEIGHT'])  # Set the top margin to the height of the banner
        # Set the bottom margin to (window_height - banner_height - button_height)
        self.__menu_area.set_margin_bottom(
            self.__launcher_properties['LAUNCHER_HEIGHT'] - self.__launcher_properties['BANNER_HEIGHT'] -
            self.__launcher_properties['CONFIG_BUTTON_HEIGHT'])
        self.__build_menu_buttons()  # Construct a list of buttons to add to the configuration menu
        self.__layout_container.attach(child=self.__menu_area, left=0, top=1, width=1, height=1)
        for index, button in enumerate(self.__menu_buttons, start=0):
            self.__menu_area.pack_start(child=self.__menu_buttons[button].get_button(), expand=False, fill=False, padding=0)

    def __build_menu_buttons(self) -> None:
        """ Private Initializer: This function builds the menu buttons and assigns CSS class definitions. """
        for i in range(len(launcher_configuration_menu_labels)):
            if i == self.__active_menu:
                self.__menu_buttons[launcher_configuration_menu_labels[i]] = L_Button(self, launcher_configuration_menu_labels[i], i, self.__menu_button_css_class, self.__menu_button_css_active)
            else:
                self.__menu_buttons[launcher_configuration_menu_labels[i]] = L_Button(self, launcher_configuration_menu_labels[i], i, self.__menu_button_css_class, self.__menu_button_css_inactive)

    def process_menu_selection(self, button_number) -> None:
        """ Public Processor: This function coordinates menu actions. """
        self.__activate_menu_button(button_number)
        self.__active_menu = button_number

    def __activate_menu_button(self, button_number):
        """ Private Initializer: This function modifies CSS style attributes for active and inactive menu buttons. """
        if self.__active_menu != button_number:
            self.__menu_buttons[launcher_configuration_menu_labels[button_number]].set_style_name(self.__menu_button_css_active)
            self.__menu_buttons[launcher_configuration_menu_labels[self.__active_menu]].set_style_name(self.__menu_button_css_inactive)