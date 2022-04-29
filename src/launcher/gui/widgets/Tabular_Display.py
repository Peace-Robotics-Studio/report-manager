#  Tabular_Display.py. (Modified 2022-04-28, 11:06 p.m. by Praxis)
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
    }
    TOGGLE_BUTTONS = {}
    def __init__(self):
        """ Constructor:  """
        self.fields_in_data = []
        self.__displaying_tree_view = False
        self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.__layout_container.set_vexpand(True)
        self.__layout_container.get_style_context().add_class('table-list-container')
        self.__action_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__action_bar.get_style_context().add_class('action-bar')
        self.__action_bar.set_hexpand(True)
        # expand_button = Form_Button(name="expand", callback=self.button_clicked, tooltip_text="Expand All")
        # self.__action_bar.add(expand_button.add())
        self.register_button(name="expand", callback=self.button_clicked, tooltip="Expand All", interaction_type="toggle", group_key="display_list", active=True)
        self.register_button(name="collapse", callback=self.button_clicked, tooltip="Collapse All", interaction_type="toggle", group_key="display_list", active=False)
        # collapse_button = Form_Button(name="collapse", active=False, callback=self.button_clicked, tooltip_text="Collapse All")
        # self.__action_bar.add(collapse_button.add())
        restore_button = Form_Button(name="restore", active=False, callback=self.button_clicked, tooltip_text="Restore Defaults")
        self.__action_bar.add(restore_button.add())
        save_button = Form_Button(name="save", active=False, callback=self.button_clicked, tooltip_text="Save Changes")
        self.__action_bar.add(save_button.add())
        self.__layout_container.add(self.__action_bar)

        # Create an entry box to allow the user to modify the file path
        self.search_entry = Gtk.Entry()
        self.search_entry.get_style_context().add_class('action-bar-search')
        self.search_entry.set_placeholder_text(text="Search")

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

    def button_clicked(self, button, name):
        if name == "expand":
            self.tree_view.expand_all()
            if self.TOGGLE_BUTTONS[name]["status"] == True:
                self.__toggle_button(name)
        elif name == "collapse":
            self.tree_view.collapse_all()
            if self.TOGGLE_BUTTONS[name]["status"] == True:
                self.__toggle_button(name)

    def register_button(self, name: str, callback: callable, tooltip: str, interaction_type: str, group_key: str, active: bool):
        button = Form_Button(name=name, callback=callback, tooltip_text=tooltip, active=active)
        self.__action_bar.add(button.add())
        if interaction_type == "toggle":
            self.TOGGLE_BUTTONS[name] = {"status": active, "object": button, "group_key": group_key}

    def __toggle_button(self, name):
        if self.TOGGLE_BUTTONS[name]["status"]:  # Button is active
            self.TOGGLE_BUTTONS[name]["object"].set_inactive()  # Set this button as inactive
            self.TOGGLE_BUTTONS[name]["status"] = False  # Set its active status to False
            for button_name, properties in self.TOGGLE_BUTTONS.items():  # Loop through all registered buttons
                if properties["group_key"] == self.TOGGLE_BUTTONS[name]["group_key"]:  # Find buttons with matching group keys
                    if button_name != name:  # Exclude this button from the matches
                        # print(self.TOGGLE_BUTTONS[button_name]["status"])
                        self.__toggle_button(button_name)
        else:
            self.TOGGLE_BUTTONS[name]["object"].set_active()
            self.TOGGLE_BUTTONS[name]["status"] = True


    def get_layout_container(self) -> Gtk.Container:
        """ Public Accessor: Returns Gtk.Container object. """
        return self.__layout_container

    def add(self, widget: Gtk.Container):
        self.list_container.add(widget)

    def create_tree_view(self, data: dict, gtypes: list):
        # Create a TreeStore using a list of column types (required to initialize storage containers)
        self.tree_store = Gtk.TreeStore.new(types=gtypes)
        self.update_treestore(data)  # Format the data and store it in TreeStore container

        # Use an internal column for filtering
        self.filter = self.tree_store.filter_new()
        self.filter.set_visible_column(column=self.COLUMNS["VISIBLE"])
        # Create a new TreeView and assign it a model (data store)
        self.tree_view = Gtk.TreeView(model=self.filter)
        self.tree_view.get_style_context().add_class('treeview')
        self.tree_view.connect("cursor-changed", self.test)
        # self.tree_view.set_headers_visible(False)

        # Standard text renderer
        renderer_text = Gtk.CellRendererText()
        renderer_text.set_padding(0, 0)

        # An editable text field to be used for 'Usual Name'
        renderer_editable_text = Gtk.CellRendererText()
        renderer_editable_text.set_property("editable", True)
        renderer_editable_text.connect("edited", self.text_edited)
        renderer_editable_text.set_padding(0, 0)

        liststore_manufacturers = Gtk.ListStore(str)
        manufacturers = ["M", "F"]
        for item in manufacturers:
            liststore_manufacturers.append([item])

        renderer_combo = Gtk.CellRendererCombo()  # Inherits from Gtk.CellRendererText
        renderer_combo.set_property("editable", True)  # Whether the text can be modified by the user
        renderer_combo.set_property("model", liststore_manufacturers)  # Model containing the possible values for the combo box
        renderer_combo.set_property("text-column", 0)  # Column in the data model to get the strings from
        renderer_combo.set_property("has-entry", False)  # False: don't allow any strings other than in the registered model, despite being editable
        renderer_combo.connect("edited", self.on_combo_changed)  # not 'changed'? 'edited' is the signal connected to CellRendererText

        # Loop through the generated list of data fields and create columns for some of them.
        for column_number, column_title in enumerate(list(self.COLUMNS.keys())[1:], start=1):  # Start count at 1, ignoring the 'visible' bool field.
            if column_title != 'Last' and column_title != 'First':  # Ignore these fields. They are for data access convenience.
                if column_title == 'Identity':
                    column_combo = Gtk.TreeViewColumn(title=column_title)
                    column_combo.pack_start(cell=renderer_combo, expand=False)
                    column_combo.add_attribute(renderer_combo, "text", column_number)
                    self.tree_view.append_column(column=column_combo)
                elif column_title == 'Usual':
                    # Put the text into a TreeView column
                    column_editable = Gtk.TreeViewColumn(title=column_title)
                    column_editable.pack_start(cell=renderer_editable_text, expand=False)
                    column_editable.add_attribute(renderer_editable_text, "text", column_number)
                    self.tree_view.append_column(column=column_editable)
                else:
                    column = Gtk.TreeViewColumn(title=column_title)
                    column.pack_start(cell=renderer_text, expand=False)
                    column.add_attribute(renderer_text, "text", column_number)
                    self.tree_view.append_column(column=column)

        self.sw = Gtk.ScrolledWindow()
        self.sw.set_vexpand(True)
        self.sw.add(widget=self.tree_view)

        self.add(self.sw)
        self.__displaying_tree_view = True

    def on_combo_changed(self, widget, path, text):
        self.tree_store[path][self.COLUMNS['Identity']] = text

    def test(self, widget):
        model, iter = self.tree_view.get_selection().get_selected()
        # print(model.get(iter, 1, 2))

    def text_edited(self, widget, path, text):
        # self.liststore[path][1] = text
        print(f"Cell edited: {path} with {text}")

    def empty(self):
        """ Delete the TreeView from its list_container """
        contents = self.list_container.get_children()
        for widget in contents:
            widget.destroy()
        # Reset attributes list to initial values
        self.__displaying_tree_view = False
        self.COLUMNS = {"VISIBLE": 0}
        self.search_entry.set_text("")

    def update(self, data: dict):
        """ Add data to TreeStore """
        # Format the data into a usable dictionary format
        self.current_data = self.format_data(data)

        # Store a list of field names
        gtypes = [bool]  # Create a list containing column types of gtypes
        columns = list(data.keys())  # Get a list of all keys in the data dict
        columns.remove("Grade")  # Remove the 'Grade' field since it will be used as a top-level category
        for column_number, field in enumerate(columns, start=1):  # Loop through the list of field names
            self.COLUMNS[field] = column_number  # Assign a column position number to each field name. Used when adding attributes to columns
        # Create a list of types corresponding to each field name
        for item in self.current_data[next(iter(self.current_data))][0]:  # Get the first item from the list of values linked to the dictionary's first key
            gtypes.append(type(item))  # Store the gtype value for each of the components in this item
        # Create a TreeView to display the data
        if self.__displaying_tree_view is False:  # Check to see if this TreeView already exists
            self.create_tree_view(data=self.current_data, gtypes=gtypes)  # Create a new TreeView object
            self.__displaying_tree_view = True  # Record that a TreeView object exists
        else:  # TreeView created previously. Update its TreeStore
            self.update_treestore(self.current_data)  # Update the information shown by this TreeView
        self.__layout_container.show_all()  # Show all widgets

    def update_treestore(self, data):
        """ data: formatted dict of student info imported from cvs. """
        if self.__displaying_tree_view:  # This TreeView was created previously
            self.tree_store.clear()  # Clear all data from its TreeStore
        sorted_keys = sorted(data.keys())  # Sort grade keys in ascending order
        sorted_keys.remove('KF')  # Remove kindergarten from the list of keys
        self.add_values(data, 'KF')  # Add kindergarten values first
        for key in sorted_keys:  # Add values for all remaining keys
            self.add_values(data, key)  # Add each grade and associated students

    def add_values(self, data, key):
        """ Called by update_treestore(). Creates a top-level expandable category row and adds child rows. Each child row
            contains information about a single student. """
        # Create a label for the top-level row
        category_name = f"Grade {key[1] if key.startswith('0') else key} ({len(data[key])})"  # Strip any leading '0' from the key
        # Format the data used by the top-level row label
        category_list_values = [True, category_name]  # List of values for each row [Visible = True, Grade # (count)
        if len(data[key][0]) > 1:  # Check if the data for each student includes more than a string value of their name
            for i in range(len(data[key][0]) - 1):  # For each additional item in the value
                category_list_values += [""]  # Add an empty string to the top-level row name to fill column spaces
        top_level_row = self.tree_store.append(parent=None, row=category_list_values)  # Store the list 'category_list_values' in the TreeStore
        for item in data[key]:  # For each student in this grade
            self.tree_store.append(parent=top_level_row, row=[True] + item)  # Set these entries as children of the top-level row. Add the value 'True' to front of the data list.

    def format_data(self, data) -> dict:
        grade_groups = {}
        self.fields_in_data = list(data.keys())
        self.fields_in_data.remove("Grade")
        for item_number, grade in enumerate(data['Grade'], start=0):
            key = grade
            if key not in grade_groups:
                grade_groups[key] = []
            student_data = []
            for field in self.fields_in_data:
                student_data.append(data[field][item_number])
            grade_groups[key].append(student_data)
        return grade_groups

    def __get_pixbuf_image(self, image_name) -> GdkPixbuf.Pixbuf:
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
        else:  # A value has been entered into the search box
            self.tree_store.foreach(self.reset_row, False)  # Set the 'HIDDEN' field of all rows in the TreeStore to False
            search_fields_for_match = ["Name"]  # Create a list of fields to search for a query match
            if "Status" in self.fields_in_data:  # Check to see if 'Status' is a field in the data set
                search_fields_for_match.append("Status")  # Add this field to the list for matching
            self.tree_store.foreach(self.show_matches, search_fields_for_match, search_query, show_subtrees_of_matches)  # Check to see if the row value matches the search query
            self.tree_view.expand_all()  # Expand all rows to display filtered results
        self.filter.refilter()  # Trigger 'row_changed' signal to force evaluation of whether a row is visible or not based on the updated HIDDEN field

    def reset_row(self, model: Gtk.TreeModel, path: Gtk.TreePath, iter: Gtk.TreeIter, make_visible: object):
        """ Callback for Gtk.TreeModel.foreach() implementing Gtk.TreeModelForeachFunc(model, path, iter, *data) """
        # Set the value of the HIDDEN column pointed to by iter to bool value in make_visible
        self.tree_store.set_value(iter, self.COLUMNS["VISIBLE"], make_visible)  # Values: Gtk.TreeIter, int, GObject.Value

    def show_matches(self, model: Gtk.TreeModel, path: Gtk.TreePath, row_iter: Gtk.TreeIter, search_list: list, search_query, show_subtrees_of_matches: object):
        """ Callback for Gtk.TreeModel.foreach() implementing Gtk.TreeModelForeachFunc(model, path, iter, *data) """
        # User data: search_query; show_subtrees_of_matches
        for field in search_list:
            text = model.get_value(iter=row_iter, column=self.COLUMNS[field]).lower()  # Get the string value stored in the row's NAME field
            if search_query in text:  # Check to see if the search_query string is a substring of text
                # Propagate visibility change up
                self.make_path_visible(model=model, row_iter=row_iter)  # Make this row visible and search for parents to this node and make them visible
                if show_subtrees_of_matches:  # If we are showing children of this node
                    # Propagate visibility change down
                    self.make_subtree_visible(model=model, row_iter=row_iter)

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

