# coding=UTF-8

# Fluent Python
# Chapter 2: An Array of Sequences
# Key: iteration, slicing, sorting and concatenation

from collections import namedtuple


# built-in Sequences
# Container sequences: list, tuple, and collections.deque can hold items of different types
# Flat sequences: str, bytes, bytearray, memoryview, and array.arry hold items of one type

# Container sequences hold references to the objects they contain, which may be of any type,
# while flat sequences phycically store the value of each item within its own memory space.

# Mutable sequences: list, tytearray, array.array, collections.deque, and memoryview
# Immuntable sequences: tuple, str, and bytes

# List Comprehensions(listcomps) and Generator Expressions(genexps)
# A listcomps is meant to do one thing only: to build a new list.
# A genexp saves memory because it yields items one by one using the iterator protocal.
# Genexps use the same syntax as listcomps, but are enclosed in parentheses rather than brackets.

# Tuples are not just Immutable lists
# Tuples as Records
traveler_ids = [('USA','31195855'),('BRA','CE342567'),('ESP','XDA205856')]
for passport in sorted(traveler_ids):
    print('%s/%s' % passport)

for country, _ in traveler_ids:
    print(country)

# Tuple Unpacking
# Tuple unpacking works with any iterable object.
a, b = (23, 32)
a, b = b, a
# Using * to grab excess items
a, b, *rest = range(5)

# Named Tuples
City = namedtuple('City','name country population coordinates')
tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139691667))
print(tokyo.population, tokyo.coordinates)
print(City._fields)
LatLong = namedtuple('LatLong','Lat Long')
delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889, 77.208889))
delhi = City._make(delhi_data)
print(delhi._asdict())
for key, value in delhi._asdict().items():
    print(key + ':', value)

# Tuples as Immutable Lists

# Slicing
# Slice Objects
s = 'bicycle'
ran = slice(2,7)
print(s[ran])

# Multidimensional Slicing and Ellipsis: to check in numpy

# list.sort and sorted built-in Function
# The list.sort method sorts a list in place - that is, without making a copy.
# It returns None and does not create a new list.
# This is an important Python API convention: functions or methods that change an object
# in place should return None to make it clear to the caller that the object itself was changed.
# In contrast, the built-in function sorted creates a new list and returns it.
# Both take two optional, keyword-only arguments: reverse and key.

# Managing Ordered Sequences with bisect
# The bisect module offers two main functions - bisect and insort - that use the binary search
# algorithm to quickly find and insert items in any sorted sequence.

# When a list is not the answer
# If the list will only contain numbers, an array.array is more efficient than a list:
# it supports all mutable sequence operations(including .pop, .insert, and .extend), and
# additional methods for fast loading and saving such as .frombytes and .tofile.

from array import array
from random import random

floats = array('d', (random() for i in range(10**6)))
print(floats[-1])

# The built-in memorview class is a shared-memory sequence type that lets you
# handle slices of arrays without copying bytes.

# If you are doing advanced numeric processing in arrays, you should using the NumPy and Scipy libraries.

# Since inserting and removing from the left of a list is costly because the entire list must be shifted,
# the class collections.deque is a thread-safe double-ended queue designed for fast inserting
# and removing from both ends.

from collections import deque
dq = deque(range(10),maxlen=10)
print(dq)

















