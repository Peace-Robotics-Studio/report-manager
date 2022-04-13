# L_Menu_Layer.py
#
# Copyright 2022 Peace Robotics Studio

import cairo
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk

class L_Menu_Layer:

    def __init__(self, launcher_properties):
        """ Constructor """
        self.__launcher_properties = launcher_properties
        self.__layout_container = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        self.__build_layer()

    def get_layout_container(self) -> Gtk.Grid:
        """ Public Accessor: This function returns the Gtk layout container """
        return self.__layout_container

    def __build_layer(self) -> None:
        """ Private Initilizer: This function composes the menu layout """
        self.__menu_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.__menu_area.get_style_context().add_class('content')
        self.__menu_area.set_hexpand(True)
        self.__menu_area.set_vexpand(True)
        self.__menu_area.set_margin_top(self.__launcher_properties['BANNER_HEIGHT'])

        self.__layout_container.attach(child=self.__menu_area, left=0, top=1, width=1, height=1)
        # for index, button in enumerate(self.__menu_buttons, start=0):
        #     self.__layout_container.attach(child=button, left=1, top=index, width=1, height=1)