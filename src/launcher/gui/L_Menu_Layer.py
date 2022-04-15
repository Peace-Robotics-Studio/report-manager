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
        self.__active_menu = default_launcher_menu_tab
        self.__menu_container_css_class = 'launcher-menu-container'
        self.__menu_button_css_class = 'launcher-menu-bar'
        self.__menu_button_css_active = 'active-button'
        self.__menu_button_css_inactive = 'inactive-button'
        self.__layout_container = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        self.__build_layer() # Initialization step

    # Private Methods

    def __activate_menu_button(self, menu_key: str):
        """ Private Initializer: This function modifies CSS style attributes for active and inactive menu buttons. """
        if self.__active_menu != menu_key:
            self.__menu_buttons[menu_key].set_style_name(self.__menu_button_css_active)
            self.__menu_buttons[self.__active_menu].set_style_name(self.__menu_button_css_inactive)

    def __build_layer(self) -> None:
        """ Private Initializer: This function composes the menu layout """
        self.__menu_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__menu_area.get_style_context().add_class(self.__menu_container_css_class)
        self.__menu_area.set_hexpand(True)
        self.__menu_area.set_vexpand(True)
        self.__menu_area.set_margin_top(self.__launcher_properties['BANNER_HEIGHT'])  # Set the top margin to the height of the banner
        # Set the bottom margin to (window_height - banner_height - button_height)
        self.__menu_area.set_margin_bottom(
            self.__launcher_properties['LAUNCHER_HEIGHT'] - self.__launcher_properties['BANNER_HEIGHT'] -
            self.__launcher_properties['MENU_BUTTON_HEIGHT'])

        self.__build_menu_buttons()  # Construct a list of buttons to add to the configuration menu
        self.__layout_container.attach(child=self.__menu_area, left=0, top=1, width=1, height=1)
        for menu_key in self.__menu_buttons:
            self.__menu_area.pack_start(child=self.__menu_buttons[menu_key].get_button(), expand=False, fill=False, padding=0)

    def __build_menu_buttons(self) -> None:
        """ Private Initializer: This function builds the menu buttons and assigns CSS class definitions. """
        for menu_key in launcher_configuration_menu_labels:
            if menu_key == self.__active_menu:
                self.__menu_buttons[menu_key] = L_Button(self, launcher_configuration_menu_labels[menu_key], menu_key, self.__menu_button_css_class, self.__menu_button_css_active)
            else:
                self.__menu_buttons[menu_key] = L_Button(self, launcher_configuration_menu_labels[menu_key], menu_key, self.__menu_button_css_class, self.__menu_button_css_inactive)

    # Public Methods

    def get_layout_container(self) -> Gtk.Grid:
        """ Public Accessor: This function returns the Gtk layout container """
        return self.__layout_container

    def process_menu_selection(self, menu_key) -> None:
        """ Public Processor: This function coordinates menu actions with the GUI_Manager. """
        self.__activate_menu_button(menu_key)
        self.__active_menu = menu_key
        self.__h_gui_manager.load_content_area(menu_key)

