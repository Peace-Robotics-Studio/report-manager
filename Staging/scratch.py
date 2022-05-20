#  scratch.py. (Modified 2022-05-19, 10:51 p.m. by Praxis)
#  Copyright (c) 2022-2022 Peace Robotics Studio
#  Licensed under the MIT License.
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so.

import xml.etree.ElementTree as ET


with open(launcher_help_xml_file) as file:
    tree = ET.parse(file)
root = tree.getroot()

""" Parse the contents of XML document and save as dict """
help_pages = {}
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
                for child_element in element:   # Loop through all elements in 'section'
                    # Clean text of all whitespace characters
                    text = child_element.text  # Grab the text from this child_element element
                    if text is not None:  # Make sure that the element contained text
                        text = " ".join(str(text).split())  # Remove any leading \n, \t, or multiple spaces
                    # Add to the dict
                    help_pages[tab.get("id")][page.get('id')][element.tag][count][child_element.tag] = {"attrib": child_element.attrib, "text": text}
            else:
                # Create a dict with 'attribute' key and set to the dict of element attributes
                help_pages[tab.get("id")][page.get('id')][element.tag] = dict(attribute=element.attrib)
                # Add a 'text' key to this dict and set it to string contained by the element
                help_pages[tab.get("id")][page.get('id')][element.tag]["text"] = element.text
print(help_pages)