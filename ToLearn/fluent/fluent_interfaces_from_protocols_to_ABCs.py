# coding=UTF-8

# Fluent Python
# Chapter 11: Interfaces: From Protocols to ABCs

# An abstract class represents an interface.

# Interfaces and Protocols in Python Culture

class Vector2d:
    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y))

# We turned x and y into read-only properties.

# An interface seen as a set of methods to fulfill a role is what Smalltalkers called a procotol,
# and the term spread to other dynamic language communities. Protocols are independent of inheritance.
# A class may implement several protocols, enabling its instances to fulfill several roles.

# One of the most fundamental interfaces in Python is the sequence protocol.

# Python Digs Sequences
# The philosophy of the Python data model is to cooperate with essential protocols as much as possible.




