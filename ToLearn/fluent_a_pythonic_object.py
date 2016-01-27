# coding=UTF-8

# Fluent Python
# Chapter 9: A Pythonic Object

# Object Representations
# repr(): Return a string representing the object as the developer wants to see it.
# str(): Return a string representing the object as the user wants to see it.

# As you know, we implement the special methods __repr__ and __str__ to support repr() and str().
# There are two additional special methods to support alternative representations of objects: __bytes__ and __format__.

from array import array
import math

class Vector2d:
    typecode = 'd'

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(array(self.typecode, self)))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

v1 = Vector2d(3, 4)
print(v1)
print(repr(v1))
print(bytes(v1))

# A Hashable Vector2d
# As defined, so far our Vector2d instances are unhashable, so we can’t put them in a set.
# To make a Vector2d hashable, we must implement __hash__ (__eq__ is also required).

# Saving Space with the __slots__ Class Attribute
# If you are dealing with millions of instances with few attributes, the __slots__ class attribute
# can save a lot of memory, by letting the interpreter store the instance attributes in a tuple instead of a dict.











