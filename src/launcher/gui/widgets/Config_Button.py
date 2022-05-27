import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from .Context_Box import Context_Box
from .Form_Item import Form_Item_Properties


class Config_Button:
    def __init__(self, css_class: str, css_name: str, parent_window: Gtk.Window, label: str = None):
        self.__parent_window = parent_window
        self.__menu_items = []
        self.drop_config_button = Gtk.Button()
        if label is not None:
            self.drop_config_button.set_label(label=label)
        self.drop_config_button.get_style_context().add_class(css_class)
        self.drop_config_button.set_name(css_name)
        self.drop_config_button.connect("clicked", self.__picker_config_context)

    def get_button(self):
        return self.drop_config_button

    def add_menu_item(self, label: str, response_key: str, callback: callable, active: bool = True, toggled_on: bool = False, decorator: str = None, title: bool = False, menu: bool = False):
        self.__menu_items.append(Form_Item_Properties(label=label, response_key=response_key, callback=callback, active=active, toggled_on=toggled_on, decorator=decorator, title=title, menu=menu))

    def __picker_config_context(self, button):
        """ Private Callback: This function creates a context menu when the picker config button is activated. """
        config_context = Context_Box(parent=self.__parent_window, reference_widget=button, align="right", form_items=self.__menu_items)
        response = config_context.run()
        # if response == Gtk.ResponseType.OK:
        #     print("The OK button was clicked")
        config_context.destroy()