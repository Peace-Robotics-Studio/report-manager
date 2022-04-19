#  Combo_Picker.py. (Modified 2022-04-18, 10:49 p.m. by Praxis)
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
from gi.repository import Gtk, Gdk
from .Context_Box import Context_Box
from ....Settings import *


class Combo_Picker:
    def __init__(self, label: str, parent_window: Gtk.Window):
        """ Constructor
            This class a custom entry field using Gtk.Entry
            label: descriptive name of the event box  """
        self.__parent_window = parent_window  # Required by the Gtk.Dialog class definition
        if "student_roster" in config_data:  # Check to see if a dictionary key for 'student roster' exists in the loaded configuration key
            self.directory_path = config_data["student_roster"]  # Set the directory_path to this key's value if it exists
        else:
            self.directory_path = ""  # Otherwise, initialize directory_path with an empty string
        self.__layoutContainer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)  # Create a root container for the combo_picker widget
        self.__layoutContainer.set_hexpand(True)  # Set the widget to stretch across the available horizontal space
        directory_label = Gtk.Label(label=label)  # Create a label to place before the directory path container
        directory_label.get_style_context().add_class('launcher-widget-label')  # Connect a CSS class to the label
        self.__layoutContainer.pack_start(child=directory_label, expand=False, fill=False, padding=0)  # Add the label to the root container

        file_dir = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        file_dir.get_style_context().add_class('launcher-widget-path-box')
        file_dir.set_hexpand(True)
        self.__layoutContainer.pack_start(file_dir, True, True, 0)

        self.path_edit_sentinel = Gtk.EventBox()
        self.path_edit_sentinel.connect('button-press-event', self.__path_box_clicked)
        file_dir.pack_start(child=self.path_edit_sentinel, expand=True, fill=True, padding=0)

        self.file_dir_entry = Gtk.Entry()
        self.file_dir_entry.add_events(Gdk.EventMask.FOCUS_CHANGE_MASK | Gdk.EventMask.KEY_RELEASE_MASK)
        self.file_dir_entry.connect("focus-out-event", self.__entry_focus_lost)
        self.file_dir_entry.connect("key-release-event", self.__entry_key_release)
        self.file_dir_entry.get_style_context().add_class('launcher-widget-entry-insert')
        self.file_dir_entry.set_has_frame(False)
        self.file_dir_entry.set_max_width_chars(100)
        self.file_dir_entry.set_can_focus(False)
        self.__update_displayed_path(False)

        self.path_edit_sentinel.add(self.file_dir_entry)

        picker_button = Gtk.Button()
        picker_button.get_style_context().add_class('launcher-widget-button-image')
        picker_button.set_can_focus(False)
        picker_button.set_name("picker-button")
        picker_button.connect("clicked", self.__file_picker)
        picker_button.set_tooltip_text("This is a tooltip")
        file_dir.pack_end(child=picker_button, expand=False, fill=False, padding=0)

        drop_config_button = Gtk.Button()
        drop_config_button.get_style_context().add_class('launcher-widget-button-image')
        drop_config_button.set_name("drop-config-button")
        drop_config_button.connect("clicked", self.__picker_config_context)
        self.__layoutContainer.pack_end(child=drop_config_button, expand=False, fill=False, padding=0)

    # Public Methods

    def get_layout_container(self) -> Gtk.Container:
        """ Public Accessor: Returns Gtk.Container object. """
        return self.__layoutContainer

    # Private Methods

    def __picker_config_context(self, button):
        dialog = Context_Box("This is the second dialog's message.")
        response = dialog.run()
        # if response == Gtk.ResponseType.OK:
        #     print("The OK button was clicked")
        dialog.destroy()

    def __path_box_clicked(self, widget, event):
        """ Private Callback: This function is triggered by a Gtk.EventBox containing the Gtk.Entry widget. """
        if 'GDK_BUTTON_PRESS' in str(event.type):  # If the user made a "single click"
            if event.button == Gdk.BUTTON_PRIMARY:  # If it is a left click
                # https://developer.gnome.org/gtk3/stable/GtkContainer.html
                #  = widget.get_children()[0].get_text()
                self.__make_path_editable()

    def __update_displayed_path(self, active_state):
        """ Private Initializer: This function sets the text in the Gtk.Entry widget. """
        if self.directory_path == "":
            self.file_dir_entry.set_placeholder_text("Select a CSV file")
        else:

            self.file_dir_entry.set_text(self.directory_path)
            self.file_dir_entry.set_position(len(self.directory_path))
            self.__set_entry_text_colour(is_valid=self.__is_path_valid(), active_state=active_state)

    def __make_path_editable(self):
        """ Private Task: This function modifies the Gtk.Entry widget so that the directory path can be edited. """
        self.__set_entry_text_colour(is_valid=self.__is_path_valid(), active_state=True)
        self.file_dir_entry.set_editable(True)
        self.file_dir_entry.set_can_focus(True)
        self.file_dir_entry.grab_focus_without_selecting()

    def __entry_focus_lost(self, widget, event):
        """ Private Callback: This function is triggered by the Gtk.Entry widget losing keyboard focus. """
        self.file_dir_entry.set_editable(False)
        self.file_dir_entry.set_can_focus(False)
        self.__set_entry_text_colour(is_valid=self.__is_path_valid(), active_state=False)
        # ToDo: Save the path to database or file for future runs

    def __entry_key_release(self, widget, event):
        """ Private Callback: This function is triggered by a keyboard key being released while focused on the Gtk.Entry widget. """
        self.directory_path = self.file_dir_entry.get_text()
        self.__set_entry_text_colour(is_valid=self.__is_path_valid(), active_state=True)

    def __is_path_valid(self) -> bool:
        """ Private Task: This function checks to see if the directory string is a valid path. """
        return os.path.exists(self.directory_path)

    def __set_entry_text_colour(self, is_valid, active_state):
        """ Private Task: This function modifies the colour of text in the Gtk.Entry box by assigning different CSS names. """
        if is_valid is True:
            if active_state is True:
                self.file_dir_entry.set_name("active-valid")
            else:
                self.file_dir_entry.set_name("inactive-valid")
        else:
            if active_state is True:
                self.file_dir_entry.set_name("active-invalid")
            else:
                self.file_dir_entry.set_name("inactive-invalid")

    def __file_picker(self, widget):
        """ Private Callback: This function instantiates and invokes a Gtk.FileChooserAction dialog window.
            widget: Parameter passed by the Gtk event loop as a result of this function being assigned as the callback for the picker button. """
        # Instantiate the FileChooserDialog object
        dialog = Gtk.FileChooserDialog(title="Please choose a file", parent=self.__parent_window, action=Gtk.FileChooserAction.OPEN)
        # Add buttons to the dialog's action bar
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,  # Add a cancel button
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,  # Add an open button
            Gtk.ResponseType.OK,
        )
        # Create a filter for csv files
        filter_py = Gtk.FileFilter()
        filter_py.set_name("csv files")
        filter_py.add_mime_type("text/csv")
        dialog.add_filter(filter_py)
        # Create a filter to view any file type
        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)
        # Display the dialog and store the response
        response = dialog.run()
        # Catch return from the 'open' button
        if response == Gtk.ResponseType.OK:
            self.directory_path = dialog.get_filename()  # Store the path of the selected file
            self.__update_displayed_path(True)  # Update entry box with file path and set text colour
            config_data["student_roster"] = self.directory_path  # Add path to internal dictionary of configuration data
            update_configuration_data()  # Save the internal dictionary to the configuration file
        dialog.destroy()
