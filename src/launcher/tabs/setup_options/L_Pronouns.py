#  L_Pronouns.py. (Modified 2022-04-30, 11:24 p.m. by Praxis)
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
from ...gui.widgets.Action_Frame import Action_Frame


class L_Pronouns:
    def __init__(self):
        self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        gender_list = Action_Frame(css_name="student-frame")
        gender_list.register_button(name="add", id="gender-add", callback=self.button_clicked, tooltip="Add", active=True)
        gender_list.register_button(name="remove", id="gender-remove", callback=self.button_clicked, tooltip="Remove", active=False)
        self.__layout_container.add(gender_list.get_layout_container())

        right_side = Gtk.Grid(column_spacing=0, row_spacing=0)
        right_side.set_vexpand(True)
        right_side.set_size_request(width=200, height=-1)
        self.__layout_container.add(right_side)

        identity_label = Gtk.Label(label="Identity:")
        identity_label.set_xalign(1)
        identity_label.get_style_context().add_class('entry-label')
        right_side.attach(child=identity_label, left=0, top=0, width=1, height=1)
        identity_entry = Gtk.Entry()
        identity_entry.set_placeholder_text(text="Enter label")
        identity_entry.connect("changed", self.added_gender_label)
        identity_entry.get_style_context().add_class('entry-with-label')
        identity_entry.set_hexpand(True)
        right_side.attach(child=identity_entry, left=1, top=0, width=1, height=1)

        pronouns_label = Gtk.Label(label="Pronouns:")
        pronouns_label.set_xalign(1)
        pronouns_label.get_style_context().add_class('entry-label')
        right_side.attach(child=pronouns_label, left=0, top=1, width=1, height=1)
        pronouns_entry = Gtk.Entry()
        pronouns_entry.set_placeholder_text(text="Space-separated list")
        pronouns_entry.connect("changed", self.added_gender_label)
        pronouns_entry.get_style_context().add_class('entry-with-label')
        pronouns_entry.set_hexpand(True)
        right_side.attach(child=pronouns_entry, left=1, top=1, width=1, height=1)

        student_list = Action_Frame(css_name="gender-frame")
        student_list.register_button(name="add", id="student-add", callback=self.button_clicked, tooltip="Add", active=True)
        student_list.register_button(name="remove", id="student-remove", callback=self.button_clicked, tooltip="Remove", active=False)
        student_list.register_button(name="expand", id="student-expand", callback=self.button_clicked, tooltip="Expand All", interaction_type="toggle", group_key="display_list", active=True)
        student_list.register_button(name="collapse", id="student-collapse", callback=self.button_clicked, tooltip="Collapse All", interaction_type="toggle", group_key="display_list", active=False)
        right_side.attach(child=student_list.get_layout_container(), left=0, top=2, width=2, height=1)

    def get_layout_container(self) -> Gtk.Container:
        """ Public Accessor: Returns the main Gtk.Container holding widgets for this class. """
        return self.__layout_container

    def button_clicked(self, button, id):
        print(f"Button Clicked: {id}")

    def added_gender_label(self, entry):
        print(f"entry_changed: {entry}")
