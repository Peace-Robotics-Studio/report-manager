#  Liststore_Frame.py. (Modified 2022-05-01, 11:18 p.m. by Praxis)
#  Copyright (c) 2022-2022 Peace Robotics Studio
#  Licensed under the MIT License.
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so.

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf
from ....Config import *
from .Action_Frame import Action_Frame


class Liststore_Frame(Action_Frame):


    def __init__(self, css_class: str = "table-list-container", css_name: str = None):
        """ Constructor:  """
        super().__init__(css_class=css_class, css_name=css_name)
        self.COLUMNS = {}  # {"VISIBLE": 0}
        self.__displaying_tree_view = False
        self.__treeview_css_class = 'listview'

    def __create_treeview(self, data: dict, gtypes: list, column_fields: list) -> None:
        """ Private initializer: Instantiates a TreeView object and adds display columns """
        # Create a ListStore using a list of column types (required to initialize storage containers)
        self.liststore = Gtk.ListStore.new(types=gtypes)
        self.__update_liststore(data=data, column_fields=column_fields)  # Format the data and store it in TreeStore container

        self.treeview = Gtk.TreeView(model=self.liststore)
        self.treeview.connect("cursor-changed", self.test)
        # Standard text renderer
        renderer_text = Gtk.CellRendererText()
        renderer_text.set_padding(0, 0)

        for column_number, field in enumerate(column_fields, start=0):
            column = Gtk.TreeViewColumn(field[0], renderer_text, text=column_number)
            if field[1] is True:
                column.set_expand(True)
            self.treeview.append_column(column)

        # Wrap the TreeView in a scrollable window
        scrollable_window = Gtk.ScrolledWindow()
        scrollable_window.set_vexpand(True)
        scrollable_window.add(widget=self.treeview)
        # Attach TreeView to the display window
        self.display_data(scrollable_window)
        self.__displaying_tree_view = True

    def test(self, widget):
        # model, iter = self.list_view.get_selection().get_selected()
        # print(model.get(iter, 1, 2))
        pass

    def reset(self) -> None:
        """ Public initializer: Delete the TreeView from its list_container """
        contents = self.list_container.get_children()
        for widget in contents:
            widget.destroy()
        self.__displaying_list_view = False

    def update(self, data: list, column_fields: list) -> None:
        """ Public initializer: Organizes data used for creating a TreeView, its columns, """

        # Generate column numbers for each field in the data_fields list.
        # COLUMNS[] is used by the search methods and when creating the TreeStore
        for column_number, field in enumerate(column_fields, start=0):  # Loop through the list of field names
            self.COLUMNS[field[0]] = column_number  # Assign a column position number to each field name. Used when adding attributes to columns

        # Display the data
        if self.__displaying_tree_view is False:  # Check to see if this TreeView already exists
            # A list of types to be stored in the TreeView columns is required by Gtk.TreeStore.new()
            gtypes = []
            for field in column_fields:
                gtypes.append(type(data[0][field[0]]))

            # Create the TreeView
            self.__create_treeview(data=data, gtypes=gtypes, column_fields=column_fields)  # Create a new TreeView object
            self.__displaying_tree_view = True  # Record that a TreeView object exists
        else:  # TreeView created previously. Update its TreeStore
            self.__update_liststore(data=data, column_fields=column_fields)  # Update the information shown by this TreeView
        self.show_all()  # Show all widgets

    def __update_liststore(self, data: dict, column_fields: list) -> None:
        """ Private Task:  """
        if self.__displaying_tree_view:  # This TreeView was created previously
            self.liststore.clear()  # Clear all data from its TreeStore
        # Add each row item
        for item in data:
            gender = []
            for field in column_fields:
                gender.append(item[field[0]])
            self.liststore.append(gender)




