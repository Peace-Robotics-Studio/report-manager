#  Form_Item.py. (Modified 2022-04-20, 8:14 p.m. by Praxis)
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

class Form_Item_Properties:
    """ Structure to hold form item properties. This is preferable over a standard dictionary because this approach allows for type checking and setting defaults. """
    def __init__(self, label: str, response_key: str, callback: callable, active: bool = True, toggled_on: bool = False, decorator: str = None, title: bool = False, menu: bool = False):
        self.__properties_dictionary = dict(label=label,
                                            response_key=response_key,
                                            callback=callback,
                                            active=active,
                                            toggled_on=toggled_on,
                                            decorator=decorator,
                                            title=title,
                                            menu=menu)
    def get_properties_dict(self):
        return self.__properties_dictionary

class Form_Item:
    def __init__(self, item_properties_list=None):
        """ Constructor:
            label: The text applied to the form item,
            response_key: A unique identifier used to store the response value in the configuration dictionary,
            active: Determines whether an item can be interacted with (enabled / disabled)
            toggled_on: Sets the widget's toggled state (as in checkboxes)
            callback: A function linked with each menu item (excluding static items such as category titles),
            decorator: An image or clickable widget,
            title: Sets the item as a static element if True,
            menu: Sets the item to spawn a new form."""
        if item_properties_list is None:
            item_properties_list = {"label": "Empty", "active": True, "toggled_on": True, "decorator": None, "title": False, "menu": False}
        self.__layoutContainer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.__layoutContainer.set_hexpand(True)
        item_properties = item_properties_list.get_properties_dict()
        image = None
        is_a_button = True
        if item_properties["decorator"] is not None:
            if item_properties["decorator"].endswith(".png"):
                image = self.__get_pixbuf_image(item_properties["decorator"])
                if item_properties["title"] is True:
                    is_a_button = False
                    self.__layoutContainer.pack_start(image, False, False, 0)
            elif item_properties["decorator"] == "checkbox":
                is_a_button = False
                checkbox = Gtk.CheckButton()
                checkbox.get_style_context().add_class('context-form-checkbox')
                checkbox.set_active(item_properties["toggled_on"])
                checkbox.connect("toggled", item_properties["callback"], item_properties["response_key"])
                self.__layoutContainer.pack_start(checkbox, False, False, 0)
                self.__layoutContainer.pack_start(Gtk.Label(label=item_properties["label"]), False, False, 0)
                self.__layoutContainer.get_style_context().add_class('context-form-option')
        if item_properties["title"] is True:
            is_a_button = False
            self.__layoutContainer.get_style_context().add_class('context-form-title')
            self.__layoutContainer.pack_start(Gtk.Label(label=item_properties["label"]), False, False, 0)
        else:
            self.__item = Gtk.Button()
            self.__item.get_style_context().add_class('context-box-container')
            if image is not None:
                self.__layoutContainer.pack_start(image, False, False, 0)

    # Public Methods

    def get_layout_container(self) -> Gtk.Container:
        """ Public Accessor: Returns Gtk.Container object. """
        return self.__layoutContainer

    def __get_pixbuf_image(self, image_name):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=res_dir['ICONS'] + image_name,
            width=20,
            height=20,
            preserve_aspect_ratio=True)
        return Gtk.Image.new_from_pixbuf(pixbuf)