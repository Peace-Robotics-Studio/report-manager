#  scratch.py. (Modified 2022-05-16, 10:55 p.m. by Praxis)
#  Copyright (c) 2022 Peace Robotics Studio
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
print(len(root))
print(root[1])

print(f"root.tag: {root.tag}")
print(f"root.attribute: {root.attrib}")

print("Iterating over children nodes:")
for child in root:
    print(child.tag, child.attrib)

print("Printing a specific child node:")
# print(root[0][1].text)

print("Iterate recursively over  full tree (all nested children):")
# for neighbor in root.iter('neighbor'):
#     print(neighbor.attrib)

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

element = root[0]
print(element.tag)
print(element.text)
print(element.attrib)
print(element.get("x"))