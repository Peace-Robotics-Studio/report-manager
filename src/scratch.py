#  scratch.py. (Modified 2022-04-27, 8:21 p.m. by Praxis)
#  Copyright (c) 2022 Peace Robotics Studio
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

class CellRendererTextWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="CellRendererText Example")

        self.set_default_size(400, 200)

        self.liststore = Gtk.ListStore(str, str)
        self.liststore.append(["Fedora", "http://fedoraproject.org/"])
        self.liststore.append(["Slackware", "http://www.slackware.com/"])
        self.liststore.append(["Sidux", "http://sidux.com/"])

        treeview = Gtk.TreeView(model=self.liststore)
        treeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)

        select_render = Gtk.CellRendererToggle()
        select_render.set_property('activatable', True)
        select_render.set_property("radio", True)
        select_render.connect('toggled', self.on_toggle)
        select_column = Gtk.TreeViewColumn(" %s" %('Select'), select_render, active=0)
        select_column.set_clickable(True)
        treeview.append_column(select_column)

        renderer_text = Gtk.CellRendererText()
        renderer_text.set_property("editable", True)
        column_text = Gtk.TreeViewColumn("Text", renderer_text, text=0)
        column_text.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        column_text.set_expand(True)
        treeview.append_column(column_text)

        renderer_editabletext = Gtk.CellRendererText()
        renderer_editabletext.set_property("editable", True)

        column_editabletext = Gtk.TreeViewColumn("Editable Text", renderer_editabletext, text=1)
        treeview.append_column(column_editabletext)

        renderer_editabletext.connect("edited", self.text_edited)

        self.add(treeview)

    def text_edited(self, widget, path, text):
        self.liststore[path][1] = text

    def on_toggle(self, cell, path):
        print("Toggled")

win = CellRendererTextWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()