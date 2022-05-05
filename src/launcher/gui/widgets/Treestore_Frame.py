#  Treestore_Frame.py. (Modified 2022-05-04, 10:15 p.m. by Praxis)
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


class Treestore_Frame(Action_Frame):
    EXPAND_BY_DEFAULT = False

    def __init__(self, css_class: str = "table-list-container", css_name: str = None):
        """ Constructor:  """
        super().__init__(css_class=css_class, css_name=css_name)
        self.filter = None
        self.tree_view = None
        self.tree_store = None
        self.search_in_fields = []
        self.__displaying_tree_view = False
        self.COLUMNS = {"VISIBLE": 0}
        self.__treeview_css_class = 'treeview'
        # Add the 'expand' and 'collapse' buttons
        self.register_button(name="expand", id="TF-expand", callback=self.__toggle_clicked, tooltip="Expand All", interaction_type="toggle", group_key="display_list", active=True)
        self.register_button(name="collapse", id="TF-collapse", callback=self.__toggle_clicked, tooltip="Collapse All", interaction_type="toggle", group_key="display_list", active=False)
        # Create an entry box to allow the user to modify the file path
        self.search_entry = Gtk.Entry()
        self.search_entry.get_style_context().add_class('action-bar-search')
        self.search_entry.set_placeholder_text(text="Search")
        self.search_entry.set_icon_from_pixbuf(Gtk.EntryIconPosition.PRIMARY, self.__get_pixbuf_image("search_dark.png"))
        self.search_entry.connect("changed", self.__search_query)
        self.add_to_action_bar(item=self.search_entry, pack="end")

    def __toggle_clicked(self, button: Gtk.Widget, id: str) -> None:
        """ Private callback: Called when the 'expand' or 'collapse' button is clicked. """
        if self.__displaying_tree_view:
            if id == "TF-expand":
                self.tree_view.expand_all()
            elif id == "TF-collapse":
                self.tree_view.collapse_all()

    def __create_tree_view(self, data: dict, column_properties: dict, row_order: dict, gtypes: list) -> None:
        """ Private initializer: Instantiates a TreeView object and adds display columns """
        # Create a TreeStore using a list of column types (required to initialize storage containers)
        self.tree_store = Gtk.TreeStore.new(types=gtypes)
        self.__update_treestore(data=data, row_order=row_order)  # Format the data and store it in TreeStore container
        # Use an internal column for filtering
        self.filter = self.tree_store.filter_new()
        self.filter.set_visible_column(column=self.COLUMNS["VISIBLE"])
        # Create a new TreeView and assign it a model (data store)
        self.tree_view = Gtk.TreeView(model=self.filter)
        self.tree_view.get_style_context().add_class(self.__treeview_css_class)
        self.tree_view.connect("cursor-changed", self.item_selected)
        # Standard text renderer
        renderer_text = Gtk.CellRendererText()
        renderer_text.set_padding(0, 0)
        # Editable text renderer
        renderer_editable_text = Gtk.CellRendererText()
        renderer_editable_text.set_property("editable", True)
        renderer_editable_text.connect("edited", self.text_edited)
        renderer_editable_text.set_padding(0, 0)
        # Loop through the list of column fields and create TreeView columns
        for column_title, properties in column_properties.items():
            if properties["renderer"] == "selectable":
                column_combo = Gtk.TreeViewColumn(title=column_title)
                renderer_combo = self.__get_renderer_combo(options=properties["options"], field=column_title)
                column_combo.pack_start(cell=renderer_combo, expand=False)
                column_combo.add_attribute(renderer_combo, "text", self.COLUMNS[column_title])
                self.tree_view.append_column(column=column_combo)
            elif properties["renderer"] == "editable-text":
                column_editable = Gtk.TreeViewColumn(title=column_title)
                column_editable.pack_start(cell=renderer_editable_text, expand=False)
                column_editable.add_attribute(renderer_editable_text, "text", self.COLUMNS[column_title])
                self.tree_view.append_column(column=column_editable)
            else:  # Use a 'static-text' renderer
                column = Gtk.TreeViewColumn(title=column_title)
                column.pack_start(cell=renderer_text, expand=False)
                column.add_attribute(renderer_text, "text", self.COLUMNS[column_title])
                self.tree_view.append_column(column=column)
        # Wrap the TreeView in a scrollable window
        scrollable_window = Gtk.ScrolledWindow()
        scrollable_window.set_vexpand(True)
        scrollable_window.add(widget=self.tree_view)
        # Attach TreeView to the display window
        self.display_data(scrollable_window)
        self.__displaying_tree_view = True

    def __get_renderer_combo(self, options: list, field: str) -> Gtk.CellRendererCombo:
        """ Private Initializer: Create a CellRendererCombo and set its model to be the options_list """
        # Create a ListStore to hold the combo options
        options_list = Gtk.ListStore(str)
        for item in options:
            options_list.append([item])
        # Create a CellRendererCombo
        renderer_combo = Gtk.CellRendererCombo()  # Inherits from Gtk.CellRendererText
        renderer_combo.set_property("editable", True)  # Whether the text can be modified by the user
        renderer_combo.set_property("model", options_list)  # Model containing the possible values for the combo box
        renderer_combo.set_property("text-column", 0)  # Column in the data model to get the strings from
        renderer_combo.set_property("has-entry", False)  # False: don't allow any strings other than in the registered model, despite being editable
        renderer_combo.connect("edited", self.on_combo_changed, field)  # not 'changed'? 'edited' is the signal connected to CellRendererText
        return renderer_combo

    def on_combo_changed(self, cell_renderer_combo, path, text, field):
        self.tree_store[path][self.COLUMNS[field]] = text

    def item_selected(self, widget):
        model, iter = self.tree_view.get_selection().get_selected()
        print(model.get(iter, 1, 2))

    def text_edited(self, widget, path, text):
        # self.liststore[path][1] = text
        print(f"Cell edited: {path} with {text}")

    def reset(self) -> None:
        """ Public initializer: Delete the TreeView from its list_container """
        contents = self.list_container.get_children()
        for widget in contents:
            widget.destroy()
        # Reset attributes list to initial values
        self.__displaying_tree_view = False
        self.COLUMNS = {"VISIBLE": 0}
        self.search_entry.set_text("")
        self.search_in_fields = []

    def update(self, data: dict, data_fields: list, column_properties: dict, row_order: dict) -> None:
        """ Public initializer: Organizes data used for creating a TreeView, its columns, """
        # Generate column numbers for each field in the data_fields list.
        # COLUMNS[] is used by the search methods and when creating the TreeStore
        for column_number, field in enumerate(data_fields, start=1):  # Loop through the list of field names
            self.COLUMNS[field] = column_number  # Assign a column position number to each field name. Used when adding attributes to columns
        # Display the data
        if self.__displaying_tree_view is False:  # Check to see if this TreeView already exists
            # A list of types to be stored in the TreeView columns is required by Gtk.TreeStore.new()
            gtypes = [bool]  # The initial type of 'bool' is added to the list of columns to store a row visibility flag
            # Generate a list of data types for each item that will be stored in the TreeStore -> create_tree_view()
            for item in data[next(iter(data))][0]:  # Get the first item from the list of values linked to the dictionary's first key
                gtypes.append(type(item))  # Store the gtype value for each of the components in this list
            # Search through the column_properties dictionary and register searchable TreeView columns
            for field, properties in column_properties.items():
                # Find all fields flagged as searchable and add them to the search_in_fields list
                if properties["searchable"]:
                    self.search_in_fields.append(field)
            # Create the TreeView
            self.__create_tree_view(data=data, column_properties=column_properties, gtypes=gtypes, row_order=row_order)  # Create a new TreeView object
            self.__displaying_tree_view = True  # Record that a TreeView object exists
        else:  # TreeView created previously. Update its TreeStore
            self.__update_treestore(data=data, row_order=row_order)  # Update the information shown by this TreeView
        self.show_all()  # Show all widgets

    def __update_treestore(self, data: dict, row_order: dict) -> None:
        """ Private Task:  """
        if self.__displaying_tree_view:  # This TreeView was created previously
            self.tree_store.clear()  # Clear all data from its TreeStore
        # Add each row and associated children
        for row_field, label in row_order.items():  # Add values for all remaining keys
            # Format the data used by the top-level row label
            category_list_values = [True, label]  # List of values for each row [Visible = True, Grade # (count)
            if len(data[row_field][0]) > 1:  # Check if the data for each student includes more than a string value of their name
                for i in range(len(data[row_field][0]) - 1):  # For each additional item in the value
                    category_list_values += [""]  # Add an empty string to the top-level row name to fill column spaces
            # Add the top-level row
            top_level_row = self.tree_store.append(parent=None, row=category_list_values)  # Store the list 'category_list_values' in the TreeStore
            # Attach all child rows 
            for item in data[row_field]:  # For each student in this grade
                self.tree_store.append(parent=top_level_row, row=[True] + item)  # Set these entries as children of the top-level row. Add the value 'True' to front of the data list.

    def __get_pixbuf_image(self, image_name) -> GdkPixbuf.Pixbuf:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=res_dir['ICONS'] + image_name,
            width=20,
            height=20,
            preserve_aspect_ratio=True)
        return pixbuf

    def __search_query(self, widget):
        """ Private callback: Callback for the Gtk.Entry """
        # See: https://stackoverflow.com/questions/56029759/how-to-filter-a-gtk-tree-view-that-uses-a-treestore-and-not-a-liststore
        if self.__displaying_tree_view:
            search_query = self.search_entry.get_text().lower()  # Get text from the entry widget and set to lower case
            show_subtrees_of_matches = False  # Check children of row matches
            if search_query == "":  # If the search box is empty
                self.tree_store.foreach(self.__reset_row, True)  # Iterate over the full TreeStore model and set the 'HIDDEN' column to True (Parameters: func, *user)
                if self.EXPAND_BY_DEFAULT:  # If rows are set to be expanded by default
                    self.tree_view.expand_all()  # Set the TreeView flag for all rows
                else:
                    self.tree_view.collapse_all()  # Otherwise, collapse all rows
            else:  # A value has been entered into the search box
                self.tree_store.foreach(self.__reset_row, False)  # Set the 'HIDDEN' field of all rows in the TreeStore to False
                self.tree_store.foreach(self.__show_matches, self.search_in_fields, search_query, show_subtrees_of_matches)  # Check to see if the row value matches the search query
                self.tree_view.expand_all()  # Expand all rows to display filtered results
            self.filter.refilter()  # Trigger 'row_changed' signal to force evaluation of whether a row is visible or not based on the updated HIDDEN field

    def __reset_row(self, model: Gtk.TreeModel, path: Gtk.TreePath, iter: Gtk.TreeIter, make_visible: object):
        """ Private callback: Callback for Gtk.TreeModel.foreach() implementing Gtk.TreeModelForeachFunc(model, path, iter, *data) """
        # Set the value of the HIDDEN column pointed to by iter to bool value in make_visible
        self.tree_store.set_value(iter, self.COLUMNS["VISIBLE"], make_visible)  # Values: Gtk.TreeIter, int, GObject.Value

    def __show_matches(self, model: Gtk.TreeModel, path: Gtk.TreePath, row_iter: Gtk.TreeIter, search_list: list, search_query, show_subtrees_of_matches: object):
        """ Private callback: Callback for Gtk.TreeModel.foreach() implementing Gtk.TreeModelForeachFunc(model, path, iter, *data) """
        # User data: search_query; show_subtrees_of_matches
        for field in search_list:
            text = model.get_value(iter=row_iter, column=self.COLUMNS[field]).lower()  # Get the string value stored in the row's NAME field
            if search_query in text:  # Check to see if the search_query string is a substring of text
                # Propagate visibility change up
                self.__make_path_visible(model=model, row_iter=row_iter)  # Make this row visible and search for parents to this node and make them visible
                if show_subtrees_of_matches:  # If we are showing children of this node
                    # Propagate visibility change down
                    self.__make_subtree_visible(model=model, row_iter=row_iter)

    def __make_path_visible(self, model: Gtk.TreeModel, row_iter: Gtk.TreeIter):
        """ Private task: Make the row pointed to by iter and its parent nodes visible """
        while row_iter:  # Progressively move up the tree hierarchy until reaching a toplevel node. Continue until while encounters 'None'
            self.tree_store.set_value(row_iter, self.COLUMNS["VISIBLE"], True)  # Set the value of the VISIBLE field to True
            row_iter = model.iter_parent(child=row_iter)  # Stores the iter of the parent to this node or 'None' if this row is already at the top level

    def __make_subtree_visible(self, model: Gtk.TreeModel, row_iter: Gtk.TreeIter):
        """ Private task: Make children of the row pointed to by the current row iter visible """
        for i in range(model.iter_n_children(iter=row_iter)):  # Query the number of children for this node and loop through them
            subtree = model.iter_nth_child(parent=row_iter, n=i)  # Obtain the iter for the ith child of this node
            if model.get_value(iter=subtree, column=self.COLUMNS["VISIBLE"]):  # If the value stored in the VISIBLE column is True
                # Subtree already visible
                continue  # Skips the iteration of this 'for' loop
            # Row is not already visible
            self.tree_store.set_value(subtree, self.COLUMNS["VISIBLE"], True)  # Set the value of the VISIBLE field to True
            self.__make_subtree_visible(model=model, row_iter=subtree)  # Recursive call to this function to evaluate whether the current row has children

