#  Tabular_Display.py. (Modified 2022-04-24, 10:16 p.m. by Praxis)
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
    EXPAND_BY_DEFAULT = False
    COLUMNS = {
        "VISIBLE": 0,
        "NAME": 1,
        "GENDER": 2,
        "ENROLLMENT": 3
    }
    def __init__(self, callback: callable):
        """ Constructor:  """

        self.__displaying_tree_view = False
        self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.__layout_container.set_vexpand(True)
        self.__layout_container.get_style_context().add_class('table-list-container')
        self.__action_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__action_bar.get_style_context().add_class('action-bar')
        self.__action_bar.set_hexpand(True)
        plus_button = Form_Button(name="plus", callback=callback, tooltip_text="Add student")
        self.__action_bar.add(plus_button.add())
        minus_button = Form_Button(name="minus", active=False, callback=callback, tooltip_text="Remove student")
        self.__action_bar.add(minus_button.add())
        edit_button = Form_Button(name="edit", active=False, callback=callback, tooltip_text="Edit student")
        self.__action_bar.add(edit_button.add())
        self.__layout_container.add(self.__action_bar)

        # Create an entry box to allow the user to modify the file path
        self.search_entry = Gtk.Entry()
        self.search_entry.get_style_context().add_class('action-bar-search')

        self.search_entry.set_icon_from_pixbuf(Gtk.EntryIconPosition.PRIMARY, self.__get_pixbuf_image("search_dark.png"))
        self.search_entry.connect("changed", self.search_query)
        self.__action_bar.pack_end(self.search_entry, False, False, 0)

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

    def create_tree_view(self, data: dict):

        self.tree_store = Gtk.TreeStore(bool, str, str, str)
        self.update_liststore(data)

        # Use an internal column for filtering
        self.filter = self.tree_store.filter_new()
        self.filter.set_visible_column(column=self.COLUMNS["VISIBLE"])

        self.tree_view = Gtk.TreeView(model=self.filter)
        self.tree_view.get_style_context().add_class('treeview')
        self.tree_view.set_headers_visible(False)

        text_renderer = Gtk.CellRendererText()
        text_renderer.set_padding(0, 0)

        for column_number, column_title in enumerate(list(self.COLUMNS.keys())[1:], start=1):
            # Put the text into a column
            col_combined = Gtk.TreeViewColumn(title=column_title)
            col_combined.pack_start(cell=text_renderer, expand=False)
            col_combined.add_attribute(text_renderer, "text", column_number)
            self.tree_view.append_column(column=col_combined)

        self.sw = Gtk.ScrolledWindow()
        self.sw.set_vexpand(True)
        self.sw.add(widget=self.tree_view)

        self.add(self.sw)
        self.__displaying_tree_view = True

    def update(self, data: dict):
        self.current_data = self.format_data(data)
        if self.__displaying_tree_view is False:
            self.create_tree_view(self.current_data)
            self.__displaying_tree_view = True
        else:
            self.update_liststore(self.current_data)
        self.__layout_container.show_all()

    def update_liststore(self, data):
        if self.__displaying_tree_view:
            self.tree_store.clear()
        sorted_keys = sorted(data.keys())  # Sort grade keys in ascending order
        sorted_keys.remove('KF')  # Remove kindergarten from the list of keys
        self.add_values(data, 'KF')  # Add kindergarten values first
        for key in sorted_keys:  # Add values for all remaining keys
            self.add_values(data, key)

    def add_values(self, data, key):
        # Strip any leading '0' from the key
        category_name = f"Grade {key[1] if key.startswith('0') else key} ({len(data[key])})"
        # Arrange the data used in the top-level row label
        category_list_values = [True, category_name]  # The base list of values for each row
        if len(data[key][0]) > 1:  # Check if the data value comprises more than a single string
            for i in range(len(data[key][0]) - 1):  # For each additional item in the value
                category_list_values += [""]  # Add an empty string
        top_level_row = self.tree_store.append(parent=None, row=category_list_values)  # Store the list 'category_list_values' in the TreeStore
        for item in data[key]:  # For each item in value
            self.tree_store.append(parent=top_level_row, row=[True] + item)  # Make these items children of the top-level row. Adds the value 'True' to front of the list.

    def format_data(self, data):
        grade_groups = {}
        for item_number, grade in enumerate(data['Grade'], start=0):
            key = grade
            if key not in grade_groups:
                grade_groups[key] = []
            grade_groups[key].append([data['Name'][item_number], data['Gender'][item_number], data['EnrStatus'][item_number]])
        return grade_groups

    def __get_pixbuf_image(self, image_name):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=res_dir['ICONS'] + image_name,
            width=20,
            height=20,
            preserve_aspect_ratio=True)
        return pixbuf

    def search_query(self, widget):
        """ Callback for the Gtk.Entry """
        # See: https://stackoverflow.com/questions/56029759/how-to-filter-a-gtk-tree-view-that-uses-a-treestore-and-not-a-liststore
        search_query = self.search_entry.get_text().lower()  # Get text from the entry widget and set to lower case
        show_subtrees_of_matches = False  # Check children of row matches
        if search_query == "":  # If the search box is empty
            self.tree_store.foreach(self.reset_row, True)  # Iterate over the full TreeStore model and set the 'HIDDEN' column to True (Parameters: func, *user)
            if self.EXPAND_BY_DEFAULT:  # If rows are set to be expanded by default
                self.tree_view.expand_all()  # Set the TreeView flag for all rows
            else:
                self.tree_view.collapse_all()  # Otherwise, collapse all rows
        else:  # Something is in the search box
            self.tree_store.foreach(self.reset_row, False)  # Set the 'HIDDEN' field of all rows in the TreeStore to False
            self.tree_store.foreach(self.show_matches, search_query, show_subtrees_of_matches)  # Check to see if the row value matches the search query
            self.tree_view.expand_all()  # Expand all rows to display filtered results
        self.filter.refilter()  # Trigger 'row_changed' signal to force evaluation of whether a row is visible or not based on the updated HIDDEN field

    def reset_row(self, model: Gtk.TreeModel, path: Gtk.TreePath, iter: Gtk.TreeIter, make_visible: object):
        """ Callback for Gtk.TreeModel.foreach() implementing Gtk.TreeModelForeachFunc(model, path, iter, *data) """
        # Set the value of the HIDDEN column pointed to by iter to bool value in make_visible
        self.tree_store.set_value(iter, self.COLUMNS["VISIBLE"], make_visible)  # Values: Gtk.TreeIter, int, GObject.Value

    def show_matches(self, model: Gtk.TreeModel, path: Gtk.TreePath, row_iter: Gtk.TreeIter, search_query, show_subtrees_of_matches: object):
        """ Callback for Gtk.TreeModel.foreach() implementing Gtk.TreeModelForeachFunc(model, path, iter, *data) """
        # User data: search_query; show_subtrees_of_matches
        text = model.get_value(iter=row_iter, column=self.COLUMNS["NAME"]).lower()  # Get the string value stored in the row's NAME field
        if search_query in text:  # Check to see if the search_query string is a substring of text
            # Propagate visibility change up
            self.make_path_visible(model=model, row_iter=row_iter)  # Make this row visible and search for parents to this node and make them visible
            if show_subtrees_of_matches:  # If we are showing children of this node
                # Propagate visibility change down
                self.make_subtree_visible(model=model, row_iter=row_iter)  #
            return

    def make_path_visible(self, model: Gtk.TreeModel, row_iter: Gtk.TreeIter):
        """ Make the row pointed to by iter and its parent nodes visible """
        while row_iter:  # Progressively move up the tree hierarchy until reaching a toplevel node. Continue until while encounters 'None'
            self.tree_store.set_value(row_iter, self.COLUMNS["VISIBLE"], True)  # Set the value of the VISIBLE field to True
            row_iter = model.iter_parent(child=row_iter)  # Stores the iter of the parent to this node or 'None' if this row is already at the top level

    def make_subtree_visible(self, model: Gtk.TreeModel, row_iter: Gtk.TreeIter):
        """ Make children of the row pointed to by the current row iter visible """
        for i in range(model.iter_n_children(iter=row_iter)):  # Query the number of children for this node and loop through them
            subtree = model.iter_nth_child(parent=row_iter, n=i)  # Obtain the iter for the ith child of this node
            if model.get_value(iter=subtree, column=self.COLUMNS["VISIBLE"]):  # If the value stored in the VISIBLE column is True
                # Subtree already visible
                continue  # Skips the iteration of this 'for' loop
            # Row is not already visible
            self.tree_store.set_value(subtree, self.COLUMNS["VISIBLE"], True)  # Set the value of the VISIBLE field to True
            self.make_subtree_visible(model=model, row_iter=subtree)  # Recursive call to this function to evaluate whether the current row has children

