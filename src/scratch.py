#  scratch.py. (Modified 2022-05-15, 12:26 p.m. by Praxis)
#  Copyright (c) 2022 Peace Robotics Studio
#  Licensed under the MIT License.
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so.

from types import SimpleNamespace


class ChildName:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        # instance is our parent
        return f'I am {self.name}, my parent is {instance.name}.'


class ChildDiff:
    def __init__(self, born):
        self.born = born

    @property
    def diff(self):
        return self.born - self.parent.born

    def age_diff(self):
        return f'I am {self.diff} years older than {self.parent.name}.'

    def __get__(self, instance, owner):
        print("In _get_")
        self.parent = instance  # XXX: weakref?
        return self  # expose object to be able call age_diff() etc.


class Parent:
    def __init__(self, name, born):
        self.child_name = ChildName(name='Bar')
        self.child_diff = ChildDiff(born=42)


parent = Parent(name='Foo', born=23)
print(parent.child_name)             # ... I am Bar, my parent is Foo.
print(parent.child_diff.age_diff())  # ... I am 19 years older than Foo.
