#  scratch.py. (Modified 2022-04-21, 10:25 p.m. by Praxis)
#  Copyright (c) 2022 Peace Robotics Studio
#  Licensed under the MIT License.
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so.

import gi

from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_default_size(200, 200)

        overlay = Gtk.Overlay()

        textview = Gtk.TextView()
        textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        textbuffer = textview.get_buffer()
        textbuffer.set_text("Welcome to the PyGObject Tutorial\n\nThis guide aims to provide an introduction to using Python and GTK+.\n\nIt includes many sample code files and exercises for building your knowledge of the language.", -1)
        overlay.add(textview)

        button = Gtk.Button(label="Overlayed Button")
        button.set_tooltip_text("Hello")
        #button.connect("enter-notify-event", self.on_overlay_btn_entered)
        button.set_valign(Gtk.Align.CENTER)
        button.set_halign(Gtk.Align.CENTER)
        overlay.add_overlay(button)


        self.add(overlay)
        overlay.show_all()
        self.show_all()

    def on_overlay_btn_entered(self, btn, event):
        print("Overlay button entered")
        return True


    def run(self):
        Gtk.main()


def main(args):
    mainwdw = MainWindow()
    mainwdw.run()

    return 0