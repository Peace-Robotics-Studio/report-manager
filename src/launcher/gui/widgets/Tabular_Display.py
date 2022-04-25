#  Tabular_Display.py. (Modified 2022-04-24, 8:09 p.m. by Praxis)
#  Copyright (c) 2022-2022 Peace Robotics Studio
#  Licensed under the MIT License.
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so.

import gi
import cairo

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf
from ....Config import *
from .Form_Button import Form_Button


class Tabular_Display:

    def __init__(self, callback: callable):
        """ Constructor:  """

        self.__displaying_tree_view = False
        self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.__layout_container.set_vexpand(True)
        self.__layout_container.get_style_context().add_class('table-list-container')
        self.__action_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__action_bar.get_style_context().add_class('action-bar')
        self.__action_bar.set_hexpand(True)
        plus_button = Form_Button(name="plus", callback=callback)
        self.__action_bar.add(plus_button.add())
        minus_button = Form_Button(name="minus", active=False, callback=callback)
        self.__action_bar.add(minus_button.add())
        edit_button = Form_Button(name="edit", active=False, callback=callback)
        self.__action_bar.add(edit_button.add())
        self.__layout_container.add(self.__action_bar)

        # Create an entry box to allow the user to modify the file path
        self.file_dir_entry = Gtk.Entry()
        self.file_dir_entry.get_style_context().add_class('action-bar-search')

        self.file_dir_entry.set_icon_from_pixbuf(Gtk.EntryIconPosition.PRIMARY, self.__get_pixbuf_image("search_dark.png"))
        self.file_dir_entry.connect("changed", self.__entry_key_release)
        self.__action_bar.pack_end(self.file_dir_entry, False, False, 0)

        self.list_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.list_container.get_style_context().add_class('table-list-data')
        self.__layout_container.add(self.list_container)
        self.list_container.set_hexpand(True)
        self.list_container.set_vexpand(True)

        instructions = Gtk.Label()
        instructions.set_xalign(0)
        instructions.set_markup("<a href=\"https://github.com/Peace-Robotics-Studio/report-manager/wiki/Feature-Guide\" "
                   "title=\"Report Manager Wiki\">Instructions for exporting student data from MyEd BC</a>")
        instructions.get_style_context().add_class('instructions-link')
        self.__layout_container.add(instructions)

    def get_layout_container(self) -> Gtk.Container:
        """ Public Accessor: Returns Gtk.Container object. """
        return self.__layout_container

    def add(self, widget: Gtk.Container):
        self.list_container.add(widget)

    def __entry_key_release(self, widget):
        """ Private Callback: This function is triggered by a keyboard key being released while focused on the Gtk.Entry widget. """
        pass

    def create_tree_view(self, data: dict):

        grade_groups = self.format_data(data)

        self.treestore = Gtk.TreeStore(bool, str, str, str)
        self.update_liststore(grade_groups)

        self.treeview = Gtk.TreeView(model=self.treestore)
        self.treeview.expand_all()
        self.treeview.get_style_context().add_class('treeview')
        self.treeview.set_headers_visible(False)
        print(self.current_data)
        for i in range(len(data)):
            renderer = Gtk.CellRendererText()
            renderer.set_padding(0, 0)
            column = Gtk.TreeViewColumn(cell_renderer=renderer, text=i)
            self.treeview.append_column(column)

        self.add(self.treeview)
        self.__displaying_tree_view = True

    def update(self, data: dict):
        self.current_data = self.format_data(data)
        # if self.__displaying_tree_view is False:
        #     self.create_tree_view(data)
        #     self.__displaying_tree_view = True
        # else:
        #     self.update_liststore(self.current_data)
        # self.__layout_container.show_all()

    def update_liststore(self, data):
        if self.__displaying_tree_view:
            self.treestore.clear()

        label = [True, "Grade 1", "", ""]
        cat_iter = self.treestore.append(None, label)
        # for student in data['01']:
        #     self.treestore.append(cat_iter, student)

    def format_data(self, data):
        grade_groups = {}
        for item_number, grade in enumerate(data['Grade'], start=0):
            if grade not in grade_groups:
                grade_groups[grade] = []
            grade_groups[grade].append([data['Name'][item_number], data['Gender'][item_number], data['EnrStatus'][item_number]])
            print(grade_groups)
        return grade_groups

    def __get_pixbuf_image(self, image_name):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=res_dir['ICONS'] + image_name,
            width=20,
            height=20,
            preserve_aspect_ratio=True)
        return pixbuf