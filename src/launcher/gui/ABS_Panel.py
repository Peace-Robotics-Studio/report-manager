import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from abc import ABC, abstractmethod
from ..tabs.L_Help_Manager import L_Help_Manager

class Panel(ABC):

    def __init__(self, panel_name: str, page_id: dict, layout_orientation: Gtk.Orientation):
        """ Constructor """
        self.__layout_container = Gtk.Box(orientation=layout_orientation)
        self.__layout_container.set_hexpand(True)
        self.__layout_container.set_vexpand(True)
        L_Help_Manager.register_panel(panel_name=panel_name, tab_id=page_id['TAB_ID'], panel_id=page_id['PANEL_ID'])

    def get_layout_container(self):
        """ Public Accessor: Returns the main Gtk.Container holding widgets for this class. """
        return self.__layout_container

    def add(self, container: Gtk.Widget):
        self.__layout_container.add(container)

    def pack_start(self, child: Gtk.Widget, expand: bool, fill: bool, padding: int):
        self.__layout_container.pack_start(child=child, expand=expand, fill=fill, padding=padding)

    def show_all(self):
        self.__layout_container.show_all()