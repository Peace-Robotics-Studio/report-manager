#  scratch.py. (Modified 2022-04-24, 8:25 p.m. by Praxis)
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

student_tree = {'08': [
        ['Simpson, Lisa', 'F', 'active'],
        ['Bueller, Feris', 'M', 'active'],
        ['Standish, Claire', 'F', 'active']
    ],
    '09': [
        ['Wiggum, Ralph', 'F', 'active'],
        ['Frye, Cameron', 'M', 'active'],
        ['Vernon, Richard', 'F', 'active']
    ]}


class Tabular_Display:
    EXPAND_BY_DEFAULT = True
    COLUMNS = {
        "VISIBLE": 0,
        "NAME": 1,
        "GENDER": 2,
        "ENROLLMENT": 3
    }

    def __init__(self, callback: callable):
        """ Constructor:  """
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
        # self.file_dir_entry.add_events(Gdk.EventMask.KEY_RELEASE_MASK)
        self.file_dir_entry.set_icon_from_pixbuf(Gtk.EntryIconPosition.PRIMARY, self.__get_pixbuf_image("search_dark.png"))
        self.file_dir_entry.connect("changed", self.search_query)
        self.__action_bar.pack_end(self.file_dir_entry, False, False, 0)

        # Add a content container for data
        self.list_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.list_container.get_style_context().add_class('table-list-data')
        self.__layout_container.add(self.list_container)
        self.list_container.set_hexpand(True)
        self.list_container.set_vexpand(True)

        self.create_TreeView(target_container=self.list_container)

        instructions = Gtk.Label()
        instructions.set_xalign(0)
        instructions.set_markup("<a href=\"https://github.com/Peace-Robotics-Studio/report-manager/wiki/Feature-Guide\" "
                                "title=\"Report Manager Wiki\">Instructions for exporting student data from MyEd BC</a>")
        instructions.get_style_context().add_class('instructions-link')
        self.__layout_container.add(instructions)

    def create_TreeView(self, target_container: Gtk.Container):
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
        self.treeview = Gtk.TreeView(model=self.filter)
        self.treeview.set_headers_visible(False)

        # CellRenderers for text
        text_renderer = Gtk.CellRendererText()

        # Grab a list of keys (excluding the first key) from the COLUMNS dictionary
        # Create columns for the TreeView and set their names from the dictionary
        for column_number, column_title in enumerate(list(self.COLUMNS.keys())[1:], start=1):
            # Put the text into a column
            col_combined = Gtk.TreeViewColumn(title=column_title)
            col_combined.pack_start(cell=text_renderer, expand=False)
            col_combined.add_attribute(text_renderer, "text", column_number)
            self.treeview.append_column(column=col_combined)

        # Scrolled Window in case results don't fit in the available space
        self.sw = Gtk.ScrolledWindow()
        self.sw.add(widget=self.treeview)

        # vbox.pack_start(child=self.sw, expand=True, fill=True, padding=0)
        target_container.add(self.sw)

        # Initialize filtering
        self.search_query()

    def get_layout_container(self) -> Gtk.Container:
        """ Public Accessor: Returns Gtk.Container object. """
        return self.__layout_container

    def add(self, widget: Gtk.Container):
        self.list_container.add(widget)

    def add_student_nodes(self, data: dict):
        """ Add rows to the Gtk.TreeView """
        # Grab the dictionary key and set it as the title for a top-level row
        for key, value in data.items():
            # Strip any leading '0' from the key
            category_name = f"Grade {key[1] if key.startswith('0') else key} ({len(data[key])})"
            # Arrange the data used in the top-level row label
            category_list_values = [True, category_name]  # The base list of values for each row
            if len(value) > 1:  # Check if the data value comprises more than a single string
                for i in range(len(value) - 1):  # For each additional item in the value
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
                self.treeview.expand_all()  # Set the TreeView flag for all rows
            else:
                self.treeview.collapse_all()  # Otherwise, collapse all rows
        else:  # Something is in the search box
            self.tree_store.foreach(self.reset_row, False)  # Set the 'HIDDEN' field of all rows in the TreeStore to False
            self.tree_store.foreach(self.show_matches, search_query, show_subtrees_of_matches)  # Check to see if the row value matches the search query
            self.treeview.expand_all()  # Expand all rows to display filtered results
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

    def format_data(self, data):
        grade_groups = {}
        for item_number, grade in enumerate(data['Grade'], start=0):
            if grade not in grade_groups:
                grade_groups[grade] = []
            grade_groups[grade].append([data['Name'][item_number], data['Gender'][item_number], data['EnrStatus'][item_number]])
        return grade_groups

    def __get_pixbuf_image(self, image_name):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=res_dir['ICONS'] + image_name,
            width=20,
            height=20,
            preserve_aspect_ratio=True)
        return pixbuf

    def update(self, data: dict):
        pass
        # self.current_data = data
        # if self.__displaying_tree_view is False:
        #     self.create_tree_view(data)
        #     self.__displaying_tree_view
        # else:
        #     self.update_liststore(self.format_data(data))
        # self.__layout_container.show_all()

    def update_liststore(self, data):
        if self.__displaying_tree_view:
            self.treestore.clear()

        label = [True, "Grade 1", "", ""]
        cat_iter = self.treestore.append(None, label)
        for student in data['01']:
            self.treestore.append(cat_iter, student)
        # for grade in sorted(data.keys()):
        #     category = [f"Grade {grade[1] if grade.startswith('0') else grade} ({len(data[grade])})", None, None]
        #     category_iter = self.software_liststore.append(None, category)
        #     print()
        #     # for student in data[grade]:
        #     #     print(student)
        #     for student in data[grade]:
        #         tree_iter = self.software_liststore.append(category_iter, student)