#  scratch.py. (Modified 2022-05-18, 10:42 p.m. by Praxis)
#  Copyright (c) 2022-2022 Peace Robotics Studio
#  Licensed under the MIT License.
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so.

import xml.etree.ElementTree as ET

tree = ET.parse('country_data.xml')
# >>> with open("smiley.svg") as file:
# ...     ET.parse(file)
root = tree.getroot()
print(len(root))  # 1
print(root[0])  # <Element 'tab' at

print(f"root.tag: {root.tag}")  # "help_pages"
print(f"root.attribute: {root.attrib}")  # {}

print("Iterating over children nodes in root:")
for child in root:
    print(child.tag, child.attrib)  # tab {'id': '0'}

print("Iterating over children nodes in root[0]:")
for child in root[0]:
    print(child.tag, child.attrib)  # page {'id': '00'}

print("Iterating over children nodes in root[0][0]:")
for child in root[0][0]:
    print(child.tag, child.attrib)  # title {'class': 'H2'} \n section {}
    if child.tag == "section":
        print(child[2].text)  # "Lorem ipsum dolor sit amet ..."

print("Printing a specific child node:")
print(root[0].text)

print("Iterate recursively over full tree (all nested children):")
for link in root.iter('link'):
    print(link.attrib)

# https://realpython.com/python-xml-parser/

for descendant in root.iter():
    print(descendant.tag)

tag_name = "{http://www.w3.org/2000/svg}ellipse"
for descendant in root.iter(tag_name):
    print(descendant)

# Element.findall() finds only elements with a tag which are direct children of the current element
# Element.find() finds the first child with a particular tag
# Element.text accesses the element’s text content
# Element.get() accesses the element’s attributes
# for country in root.findall('country'):
#     rank = country.find('rank').text
#     name = country.get('name')
#     print(name, rank)

# https://docs.python.org/3/library/xml.etree.elementtree.html
print("++++++++++++++++++++++++++++++++++++++++++=")
# element = root[0]
# print(element.tag)
# print(element.text)
# print(element.attrib)
# print(element.get("x"))
for tab in root.findall('tab'):  # Generate a list of tabs
    if tab.get("id") == "MENU_0":  # Pick a specific tab based on the 'id' attribute
        for page in tab.findall('page'):  # Generate a list of pages
            if page.get('id') == 'PANEL_0':
                print("yeah")
                # Iterate over this element and convert children to dictionary