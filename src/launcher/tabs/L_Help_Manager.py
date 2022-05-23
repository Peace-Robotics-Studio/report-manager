#  L_Help_Manager.py. (Modified 2022-05-22, 12:10 p.m. by Praxis)
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
from ..gui.L_Menu import L_Menu
from ..gui.widgets.Treestore_Frame import Treestore_Frame
from ..gui.L_Help_Page_Renderer import L_Help_Page_Renderer
from ..gui.L_Help_Page import L_Help_Page
from ...Config import *

from gi.repository import Gtk,  GdkPixbuf

class L_Help_Manager:
    ROW_ORDER = {}
    FORMATTED_DATA = {}
    TOP_LEVEL_ROW_PROPERTIES = {}
    DATA_FIELDS = ['Title', 'Breadcrumbs']
    COLUMN_PROPERTIES = {"Title": {"renderer": "static-text", "searchable": True}}

    def __init__(self, tab_id: str):
        self.__tab_id = tab_id
        self.__close_help_menu_callback = None
        self.__page_renderer = L_Help_Page_Renderer()
        self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.__navigation_button_css_class = 'launcher-feedback-navigation-button'

        # Create a box to hold the help topic directory
        help_directory = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        help_directory.get_style_context().add_class('launcher_help_directory')
        help_directory.set_hexpand(True)
        help_directory.set_vexpand(True)
        self.__layout_container.pack_start(help_directory, True, True, 0)
        # Add TreeView to hold a directory of help contents organized by menu tab and panel
        self.topic_treeview = Treestore_Frame(css_class="launcher_help_directory_treeview", selection_callback=self.treestore_frame_selection)
        help_directory.add(self.topic_treeview.get_layout_container())
        # Add a box to hold the contents of the help file
        help_contents = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        help_contents.get_style_context().add_class('launcher_help_content')
        help_contents.set_hexpand(True)
        help_contents.set_vexpand(True)
        self.__layout_container.pack_start(help_contents, True, True, 0)

        help_contents.add(widget=self.__page_renderer.get_layout_container())

        action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        action_box.get_style_context().add_class('launcher_help_action_bar')
        help_contents.pack_end(child=action_box, expand=False, fill=False, padding=0)

        button_grid = Gtk.Grid(column_spacing=0, row_spacing=0)
        action_box.pack_end(button_grid, False, False, 0)

        help_close = Gtk.Button(label="Close")
        help_close.get_style_context().add_class(self.__navigation_button_css_class)
        help_close.connect("clicked", self.close_button_clicked)
        button_grid.attach(child=help_close, left=0, top=0, width=1, height=1)
        data = self.__load_help_xml_file(launcher_help_xml_file)
        if data is not None:
            packaged_data = self.__package_xml_tree_data(tree=data)
            self.__build_help_pages(pages=packaged_data)

    def treestore_frame_selection(self, model, iter):
        """ Callback: Triggered when a treeview row is clicked in the help menu. Function reference is passed to Treestore_Frame(). """
        if iter:  # Make sure the iterator is valid
            # Breadcrumbs values are built as tab_id.panel_id
            (breadcrumbs,) = model.get(iter, 2)  # Unpack tuple. Column 2 contains the breadcrumb data as specified by the DATA_FIELDS dict. The TreeView class prepends a bool value containing a visiblity setting.
            if breadcrumbs != "":
                tab_id, panel_id = breadcrumbs.split(".")  # Unpack list
                self.__page_renderer.show_page(tab_id=tab_id, panel_id=panel_id)

    def __build_help_pages(self, pages: dict):
        """ Creates L_Help_Page objects for each panel element listed in L_help_pages.xml. """
        for tab_id, panels in pages.items():
            for panel_id, panel_contents in panels.items():
                help_page = L_Help_Page(tab_id=tab_id, panel_id=panel_id)
                # Page title
                help_page.set_page_title(title=panel_contents['page_title']['text'], size=panel_contents['page_title']['attribute']['class'])
                # Page sections
                for i, (section, elements) in enumerate(panel_contents['section'].items()):
                    for element in elements.items():
                        # Element is a tuple (name, dict)
                        match element[0]:
                            case "title":
                                help_page.add_section_title(title=element[1]['text'], section=i, size=element[1]['attrib']['class'])
                            case "image":
                                help_page.add_image(image_file=element[1]['attrib']['name'], height=75, section=i, path_key=element[1]['attrib']['path']+'_IMAGES')
                            case "text":
                                help_page.add_text(text=element[1]['text'], section=i)
                            case "link":
                                help_page.add_link(url=element[1]['attrib']['url'], link_text=element[1]['text'], alt_text=element[1]['attrib']['alt'], section=i)

    def __load_help_xml_file(self, xml_file):
        """ Load the L_help_pages.xml file """
        if os.path.isfile(xml_file):  # Make sure the file exists
            file_size = os.stat(xml_file).st_size
            if file_size != 0:  # Make sure the file is not empty
                try:
                    with open(xml_file) as file:
                        tree = ET.parse(file)
                        return tree
                except:
                    # ToDo: Present message to user in GUI
                    print("Unable to load help_pages XML file.")
                    return None
        else:
            print("No XML file (Config.py)")
            return None

    @classmethod
    def register_panel(cls, panel_name: str, tab_id: str, panel_id: str):
        if tab_id not in cls.FORMATTED_DATA:
            cls.FORMATTED_DATA[tab_id] = []
        cls.FORMATTED_DATA[tab_id].append([panel_name, tab_id + '.' + panel_id])  # The 'Breadcrumbs' TreeStore column stores the string "tab_id+'.'+panel_id"

    @classmethod
    def register_tab(cls, tab_name: str, tab_id: str, has_panels: bool = True):
        if tab_id not in cls.FORMATTED_DATA:
            cls.FORMATTED_DATA[tab_id] = []
        cls.ROW_ORDER[tab_id] = tab_name
        if not has_panels:
            cls.set_top_level_row_properties(tab_id=tab_id, column_name='Breadcrumbs', column_value=tab_id+'.ROOT')

    @classmethod
    def set_top_level_row_properties(cls, tab_id: str, column_name, column_value):
        """ Public Class Method: Used to specify data for specific columns in the menu's TreeStore. """
        # Example: TOP_LEVEL_ROW_PROPERTIES = {'MENU_1': {'Breadcrumbs': 'MENU_1.ROOT'}} -> Adds the value 'MENU_1.ROOT' to the 'Breadcrumbs' column in the TreeStore
        if tab_id not in cls.TOP_LEVEL_ROW_PROPERTIES:
            cls.TOP_LEVEL_ROW_PROPERTIES[tab_id] = {}
        cls.TOP_LEVEL_ROW_PROPERTIES[tab_id][column_name] = column_value

    def __package_xml_tree_data(self, tree) -> dict:
        """ Parse the contents of XML document and save as dict """
        help_pages = {}
        root = tree.getroot()  # Get the root xml element
        for tab in root.findall('tab'):  # Generate a list of tabs.
            help_pages[tab.get("id")] = {}  # Create a new dict and set it to the tab's id
            for page in tab.findall('page'):  # Generate a list of pages linked to this tab
                help_pages[tab.get("id")][page.get('id')] = {}  # Create a new dict and set it to the panel's id
                for count, element in enumerate(page):
                    # Add element values contained at the 'page_title' level inside the 'page' element
                    if element.tag == "section":  # Sections have CSS styling similar to <p></p>
                        # Check to see if the 'section' key has been added for this panel
                        if "section" not in help_pages[tab.get("id")][page.get('id')]:
                            help_pages[tab.get("id")][page.get('id')][element.tag] = {}  # Add the 'section' key and set it to an empty dict
                        # Pages may have more than one section. Differentiate using the count value
                        # Create a new empty dict and set to the count key
                        help_pages[tab.get("id")][page.get('id')][element.tag][count] = {}
                        # Add all elements from the 'section' element to a dict
                        for child_element in element:  # Loop through all elements in 'section'
                            # Clean text of all whitespace characters
                            text = child_element.text  # Grab the text from this child_element element
                            if text is not None:  # Make sure that the element contained text
                                text = " ".join(str(text).split())  # Remove any leading \n, \t, or multiple spaces
                            # Add to the dict
                            help_pages[tab.get("id")][page.get('id')][element.tag][count][child_element.tag] = {"attrib": child_element.attrib, "text": text}
                    else:
                        # Create a dict with 'attribute' key and set to the dict of element attributes
                        help_pages[tab.get("id")][page.get('id')][element.tag] = dict(attribute=element.attrib)
                        # Add a 'text' key to this dict and set it to the string contained by the element
                        help_pages[tab.get("id")][page.get('id')][element.tag]["text"] = element.text
        return help_pages

    def get_layout_container(self):
        """ Public Convenience: Returns the layout container for this object. """
        return self.__layout_container

    def set_close_help_callback(self, callback: callable):
        """ Callback Reference: Allows two buttons to trigger the same action (help button and close button) """
        # This function is executed in L_Menu_Layer after the creation of the 'main_menu' navigation menu
        self.__close_help_menu_callback = callback

    def rebuild_treeview_menu(self):
        """" Public Initializer: Reload the TreeView object displaying help menu items """
        # This function is executed in L_Menu_Layer after the creation of the 'main_menu' navigation menu
        self.topic_treeview.update(data_fields=self.__class__.DATA_FIELDS,
                              column_properties=self.__class__.COLUMN_PROPERTIES,
                              row_order=self.__class__.ROW_ORDER,
                              data=self.__class__.FORMATTED_DATA,
                              top_level_row_properties=self.__class__.TOP_LEVEL_ROW_PROPERTIES)
        self.topic_treeview.set_treeview_expanded(is_expanded=True)
        self.topic_treeview.hide_column_titles(True)

    def update(self):
        """ Get the page_renderer to display the help page registered to current combination of active tab and panel ids. """
        # Display page for the active tab_id and it's active panel (panel_id is stored in a dict indexed by tab_id
        self.__page_renderer.show_page(tab_id=L_Menu.ACTIVE_TAB, panel_id=L_Menu.ACTIVE_PANEL[L_Menu.ACTIVE_TAB])

    def close_button_clicked(self, button):
        """ Callback: Triggers the toggling logic connected with the help special button in the navigation menu """
        # This function points to L_Menu.help_button_clicked().
        self.__close_help_menu_callback()  # Call the function registered as the callback for the close button in the action bar


