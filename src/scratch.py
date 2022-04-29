#  scratch.py. (Modified 2022-04-28, 8:16 p.m. by Praxis)
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

        self.set_default_size(200, 200)

        self.liststore = Gtk.ListStore(str, str)
        self.liststore.append(["Fedora", "http://fedoraproject.org/"])
        self.liststore.append(["Slackware", "http://www.slackware.com/"])
        self.liststore.append(["Sidux", "http://sidux.com/"])

        treeview = Gtk.TreeView(model=self.liststore)

        self.completion = Gtk.EntryCompletion(model = self.liststore)
        self.completion.set_text_column(1)
        self.completion.connect('match-selected', self.renderer_match_selected)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Text", renderer_text, text=0)
        treeview.append_column(column_text)

######## CellRendererText with EntryCompletion example
        renderer_text = Gtk.CellRendererText()
        renderer_text.connect('editing-started', self.renderer_text_editing_started)
        renderer_text.connect('edited', self.text_edited)
        renderer_text.set_property("editable", True)

        column_text_autocomplete = Gtk.TreeViewColumn("Editable Text", renderer_text, text=1)
        treeview.append_column(column_text_autocomplete)

######## CellRendererCombo with EntryCompletion example
        renderer_combo = Gtk.CellRendererCombo(model = self.liststore)
        renderer_combo.set_property("text-column", 1)
        renderer_combo.connect('editing-started', self.renderer_combo_editing_started)
        renderer_combo.connect('changed', self.combo_changed)
        renderer_combo.set_property("editable", True)

        column_combo_autocomplete = Gtk.TreeViewColumn("Editable Combo", renderer_combo, text=1)
        treeview.append_column(column_combo_autocomplete)


        self.add(treeview)

    def renderer_match_selected (self, completion, model, tree_iter):
        ''' beware ! the model and tree_iter passed in here are the model from the
        EntryCompletion, which may or may not be the same as the model of the Treeview '''
        text_match =  model[tree_iter][1]
        self.liststore[self.path][1] = text_match

    def renderer_text_editing_started (self, renderer, editable, path):
        ''' since the editable widget gets created for every edit, we need to
        connect the completion to every editable upon creation '''
        editable.set_completion(self.completion)
        self.path = path # save the path for later usage

    def text_edited(self, widget, path, text):
        self.liststore[path][1] = text

    def renderer_combo_editing_started (self, renderer, combo, path):
        ''' since the editable widget gets created for every edit, we need to
        connect the completion to every editable upon creation '''
        editable = combo.get_child() # get the entry of the combobox
        editable.set_completion(self.completion)
        self.path = path # save the path for later usage

    def combo_changed (self, combo, path, tree_iter):
        ''' the path is from the treeview and the tree_iter is from the model
        of the combobox which may or may not be the same model as the treeview'''
        combo_model = combo.get_property('model')
        text = combo_model[tree_iter][1]
        self.liststore[path][1] = text

win = CellRendererTextWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()