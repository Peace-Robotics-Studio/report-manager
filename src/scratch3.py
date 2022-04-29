#  scratch3.py. (Modified 2022-04-28, 9:03 p.m. by Praxis)
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
from gi.repository import Gtk


class CellRendererComboWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="CellRendererCombo Example")

        self.set_default_size(200, 200)

        liststore_manufacturers = Gtk.ListStore(str)
        manufacturers = ["M", "F"]
        for item in manufacturers:
            liststore_manufacturers.append([item])

        self.liststore_hardware = Gtk.ListStore(str, str)
        self.liststore_hardware.append(["Television", "Samsung"])
        self.liststore_hardware.append(["Mobile Phone", "LG"])
        self.liststore_hardware.append(["DVD Player", "Sony"])

        treeview = Gtk.TreeView(model=self.liststore_hardware)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Text", renderer_text, text=0)  # text=0 means: get the text to display from column 0 of the liststore
        treeview.append_column(column_text)

        renderer_combo = Gtk.CellRendererCombo()  # Inherits from Gtk.CellRendererText
        renderer_combo.set_property("editable", True)  # Whether the text can be modified by the user
        renderer_combo.set_property("model", liststore_manufacturers)  # Model containing the possible values for the combo box
        renderer_combo.set_property("text-column", 0)  # Column in the data model to get the strings from
        renderer_combo.set_property("has-entry", False)  # False: don't allow any strings other than in the registered model, despite being editable
        renderer_combo.connect("edited", self.on_combo_changed)  # not 'changed'? 'edited' is the signal connected to CellRendererText

        column_combo = Gtk.TreeViewColumn("Combo", renderer_combo, text=1)
        treeview.append_column(column_combo)

        self.add(treeview)

    def on_combo_changed(self, widget, path, text):
        self.liststore_hardware[path][1] = text


win = CellRendererComboWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
