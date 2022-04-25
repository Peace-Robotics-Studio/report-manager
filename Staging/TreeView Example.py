#  TreeView Example.py. (Modified 2022-04-24, 9:23 p.m. by Praxis)
#  Copyright (c) 2022-2022 Peace Robotics Studio
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
from gi.repository import GLib
import signal

student_tree = {'08': [
                    ['Simpson, Lisa', 'F', 'active'],
                    ['Bueller, Feris', 'M', 'active'],
                    ['Standish, Claire', 'F', 'active'],
                    ['Wiggum, Ralph', 'M', 'active']
                ],
                '09': [
                    ['Wiggum, Ralph', 'M', 'active'],
                    ['Frye, Cameron', 'M', 'active'],
                    ['Vernon, Richard', 'F', 'active']
                ]}

class TreeViewFilteringExample(Gtk.Window):
    EXPAND_BY_DEFAULT = False
    COLUMNS = {
        "VISIBLE": 0,
        "NAME": 1,
        "GENDER": 2,
        "ENROLLMENT": 3
    }

    def __init__(self):
        # Set up window
        Gtk.Window.__init__(self, title="TreeView Filtering Demo")
        self.set_size_request(500, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(True)

        # Initialize and populate a Gtk.TreeStore
        # See: https://docs.gtk.org/gtk3/treeview-tutorial.html#adding-rows-to-a-tree-store
        self.tree_store = Gtk.TreeStore(bool, str, str, str)
        self.add_student_nodes(data=student_tree)

        # Create some boxes for laying out the different controls
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.set_homogeneous(False)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox.set_homogeneous(False)
        vbox.pack_start(hbox, False, True, 0)
        self.add(vbox)

        # A text entry for filtering
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text(text="Enter text here to filter results")
        self.search_entry.connect("changed", self.search_query)
        hbox.pack_start(child=self.search_entry, expand=True, fill=True, padding=0)

        # Use an internal column for filtering
        self.filter = self.tree_store.filter_new()
        self.filter.set_visible_column(column=self.COLUMNS["VISIBLE"])
        self.tree_view = Gtk.TreeView(model=self.filter)
        self.tree_view.set_headers_visible(False)

        # CellRenderers for text
        text_renderer = Gtk.CellRendererText()

        # Grab a list of keys (excluding the first key) from the COLUMNS dictionary
        # Create columns for the TreeView and set their names from the dictionary
        for column_number, column_title in enumerate(list(self.COLUMNS.keys())[1:], start=1):
            # Put the text into a column
            col_combined = Gtk.TreeViewColumn(title=column_title)
            col_combined.pack_start(cell=text_renderer, expand=False)
            col_combined.add_attribute(text_renderer, "text", column_number)
            self.tree_view.append_column(column=col_combined)


        # Scrolled Window in case results don't fit in the available space
        self.sw = Gtk.ScrolledWindow()
        self.sw.add(widget=self.tree_view)

        vbox.pack_start(child=self.sw, expand=True, fill=True, padding=0)

        # Initialize filtering
        self.search_query()

    def add_student_nodes(self, data: dict):
        """ Add rows to the Gtk.TreeView """
        # Grab the dictionary key and set it as the title for a top-level row
        for key, value in data.items():
            # Strip any leading '0' from the key
            category_name = f"Grade {key[1] if key.startswith('0') else key} ({len(data[key])})"
            # Arrange the data used in the top-level row label
            category_list_values = [True, category_name]  # The base list of values for each row
            if len(value[0]) > 1:  # Check if the data value comprises more than a single string
                for i in range(len(value[0])-1):  # For each additional item in the value
                    category_list_values += [""]  # Add an empty string
            top_level_row = self.tree_store.append(parent=None, row=category_list_values)  # Store the list 'category_list_values' in the TreeStore
            for item in value:  # For each item in value
                self.tree_store.append(parent=top_level_row, row=[True] + item)  # Make these items children of the top-level row. Adds the value 'True' to front of the list.

    def search_query(self, data=None):
        """ Callback for the Gtk.Entry """
        # See: https://stackoverflow.com/questions/56029759/how-to-filter-a-gtk-tree-view-that-uses-a-treestore-and-not-a-liststore
        search_query = self.search_entry.get_text().lower()  # Get text from the entry widget and set to lower case
        show_subtrees_of_matches = True  # Check children of row matches
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



win = TreeViewFilteringExample()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
# Make sure that the application can be stopped from the terminal using Ctrl-C
GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, Gtk.main_quit)
Gtk.main()