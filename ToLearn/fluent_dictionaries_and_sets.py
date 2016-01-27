# coding=UTF-8

# Fluent Python
# Chapter 3: Dictionaries and Sets

# Python dicts are highly optimized. Hash tables are the engines behind Python's high-performance dicts.
# The collections.abc module provides the Mapping and MutableMapping ABCs to formalize the interfaces
# of dict and similar types.
from collections import abc

my_dict = {}
print(isinstance(my_dict,abc.Mapping))

# What is Hashable?
# An object is hashable if it has a hash vale which never changes during its lifetime(it needs a
# __hash__() method), and can be compared to other objects(it needs and __eq__() method).
# The atomic immutable types(str, bytes, numeirc types) are all hashable.

# The basic API for mapping is quite rich.
# Handling Missing Keys with setdefault
# Every Pythonista knows that d.get(k, default) is an alternative to d[k] whenever a default value
# is more convenient than handling KeyError.

# Mappings with Flexible Key Lookup
# defaultdict: Another Take on Missing Keys
# When instantiating a defaultdict, you provide a callable that is used to produce a default value
# whenever __getitem__ is passed a nonexistent key argument.

from collections import defaultdict

s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
d = defaultdict(list)
for k, v in s:
    d[k].append(v)
print(d)
print(d['dark'])

# The mechanism that makes defaultdict work by calling default_factory is actually the __missing__
# special method, a feature supported by all standard mapping types.
# The __missing__ method is just called by __getitem__.

# A search like k in my_dict.keys() is efficient in Python 3 even for very large mappings
# because dict.keys() returns a view, which is similar to a set.

# Variations of dict








