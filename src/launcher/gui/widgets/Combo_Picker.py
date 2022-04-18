#  Combo_Picker.py. (Modified 2022-04-18, 3:34 p.m. by Praxis)
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
from ....Settings import *


class Combo_Picker():
    # Fixme: Add comments
    def __init__(self, label: str, parent_window: Gtk.Window):
        self.__parent_window = parent_window
        if "student_roster" in config_data:
            self.directory_path = config_data["student_roster"]
        else:
            self.directory_path = ""
        self.__layoutContainer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.__layoutContainer.set_hexpand(True)
        directory_label = Gtk.Label(label=label)
        directory_label.get_style_context().add_class('launcher-widget-label')  # Connect a CSS class to the label
        self.__layoutContainer.pack_start(child=directory_label, expand=False, fill=False, padding=0)

        file_dir = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        file_dir.get_style_context().add_class('launcher-widget-path-box')
        file_dir.set_hexpand(True)
        self.__layoutContainer.pack_start(file_dir, True, True, 0)

        self.path_edit_sentinel = Gtk.EventBox()
        self.path_edit_sentinel.connect('button-press-event', self.path_box_clicked)
        file_dir.pack_start(child=self.path_edit_sentinel, expand=True, fill=True, padding=0)

        self.file_dir_entry = Gtk.Entry()
        self.file_dir_entry.connect("focus-out-event", self.entry_focus_lost)
        self.file_dir_entry.connect("key-release-event", self.entry_key_release)
        self.file_dir_entry.get_style_context().add_class('launcher-widget-entry-insert')
        self.file_dir_entry.add_events(Gdk.EventMask.FOCUS_CHANGE_MASK|Gdk.EventMask.KEY_RELEASE_MASK)
        self.file_dir_entry.set_has_frame(False)
        self.file_dir_entry.set_max_width_chars(100)
        self.file_dir_entry.set_can_focus(False)
        self.update_displayed_path(False)

        self.path_edit_sentinel.add(self.file_dir_entry)

        picker_button = Gtk.Button()
        picker_button.get_style_context().add_class('launcher-widget-button-image')
        picker_button.set_can_focus(False)
        picker_button.set_name("picker-button")
        picker_button.connect("clicked", self.file_picker)
        file_dir.pack_end(child=picker_button, expand=False, fill=False, padding=0)

        drop_config_button = Gtk.Button()
        drop_config_button.get_style_context().add_class('launcher-widget-button-image')
        drop_config_button.set_name("drop-config-button")
        self.__layoutContainer.pack_end(child=drop_config_button, expand=False, fill=False, padding=0)

    def get_layout_container(self):
        return self.__layoutContainer

    def path_box_clicked(self, widget, event):
        if 'GDK_BUTTON_PRESS' in str(event.type):  # If the user made a "single click"
            if event.button == Gdk.BUTTON_PRIMARY:  # If it is a left click
                # https://developer.gnome.org/gtk3/stable/GtkContainer.html
                #  = widget.get_children()[0].get_text()
                self.make_path_editable()

    def update_displayed_path(self, active_state):
        if self.directory_path == "":
            self.file_dir_entry.set_placeholder_text("Select a CSV file")
        else:

            self.file_dir_entry.set_text(self.directory_path)
            self.file_dir_entry.set_position(len(self.directory_path))
            self.set_entry_text_colour(is_valid=self.is_path_valid(), active_state=active_state)

    def make_path_editable(self):
        self.set_entry_text_colour(is_valid=self.is_path_valid(), active_state=True)
        self.file_dir_entry.set_editable(True)
        self.file_dir_entry.set_can_focus(True)
        self.file_dir_entry.grab_focus_without_selecting()

    def entry_focus_lost(self, widget, event):
        self.file_dir_entry.set_editable(False)
        self.file_dir_entry.set_can_focus(False)
        self.set_entry_text_colour(is_valid=self.is_path_valid(), active_state=False)
        # ToDo: Save the path to database or file for future runs

    def entry_key_release(self, widget, event):
        self.directory_path = self.file_dir_entry.get_text()
        self.set_entry_text_colour(is_valid=self.is_path_valid(), active_state=True)

    def is_path_valid(self) -> bool:
        return os.path.exists(self.directory_path)

    def set_entry_text_colour(self, is_valid, active_state):
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

    def file_picker(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self.__parent_window, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.directory_path = dialog.get_filename()
            self.update_displayed_path(True)
            config_data["student_roster"] = self.directory_path
            update_configuration_data()

        dialog.destroy()

    def add_filters(self, dialog):
        filter_py = Gtk.FileFilter()
        filter_py.set_name("csv files")
        filter_py.add_mime_type("text/csv")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)