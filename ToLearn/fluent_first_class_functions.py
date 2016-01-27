# coding=UTF-8

# Fluent Python
# Chapter 5: First-Class Functions

# Functions in Python are first-class objects.

# Treating a Function Like an Object
def factorial(n):
    """returns n!
    :param int n: number
    :return: n!
    """
    return 1 if n < 2 else n*factorial(n-1)

print(factorial(42))
print(factorial.__doc__)
print(type(factorial))

fact = factorial
print(fact)
print(fact(5))
print(map(factorial,range(11)))
print(list(map(fact,range(11))))

# Higher-Order Function
# A function that takes a function as argument or returns a function as the result is a high-order function.
# One example is map, another is the built-in function sorted.
def reverse(word):
    return word[::-1]

fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
print(sorted(fruits,key=len))
print(sorted(fruits,key=reverse))

# Modern Replacements for map, filter, and reduce
# The most common use case of the reduce function is summation.

from functools import reduce
from operator import add

print(reduce(add, range(100)))

# Anonymous Functions
# The best use of anonymous functions is in the context of an argument list.

# The seven flavors of Callable Objects
# The call operator(i.e., ()) may be applied to other objects beyond user-defined functions.
# To determine whether an object is callable, use the callable() built-in function.
# The Python Data Model documentation lists seven callable types:
# User-defined functions; built-in functions;
# built-in methods: Methods implemented in C, like dict.get
# Methods: Functions defined in the body of a class
# Classes: When invoked, a class runs its __new__ method to create an instance,
# then __init__ to initialize it, and finally the instance is returned to the caller.
# Class instances: If a class defines a __call__ method, then its instances may be invoked as funtions.
# Generator functions: Functions or methods that use yield keyword.
print([callable(obj) for obj in (abs, str, 13)])

# User-defined Callable Types
import random

class BingoCage:
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('Pick from empty BingoCage')

    def __call__(self):
        return self.pick()

bingo = BingoCage(range(3))
print(bingo.pick())
print(bingo())
print(callable(bingo))

# A class implementing __call__ is an easy way to create function-like objects that have some internal
# state that must be kept across invocations, like the remaining items in the BingoCage.
# An example is a decorator. Decorators must be functions, but it is sometimes convenient to be able to
# "remember" something between calls of the decorator.
# A totally different approach to creating functions with internal state is to use closures.

# Function Introspection
print(dir(factorial))
# Like the instances of a plain user-defined class, a function uses the __dict__ attribute to store
# user attributes assigned to it.

# Function Annotations
# Python 3 provides synax to attach metadata to the parameter of a function declaration and its return value.

def clip(text:str, max_len:'int > 0'=80) -> str:
    """Return text clipped at the last space before or after max_len
    :param text:
    :param max_len:
    :return:
    """
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
        if end is None:
            end = len(text)
        return text[:end].rstrip()

print(clip.__annotations__)

# Packages for functional programming
# The operator module
# Often in functional programming it is convenient to use an arithmetic operator as a function.

from operator import mul

def fact(n):
    return reduce(lambda a, b: a*b, range(1, n+1))

def fact2(n):
    return reduce(mul, range(1, n+1))

print(fact(3))
print(fact2(3))

# The functools module brings together a handful of higher-order functions.
# The best known of them is probably reduce.
# Of the remaining functions in functools, the most useful is partial and its variation, partialmethod.
from functools import partial

triple = partial(mul, 3)
print(triple(7))
print(list(map(triple,range(1,10))))
























