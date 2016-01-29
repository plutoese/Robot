# coding=UTF-8

# Fluent Python
# Chapter 7: Function Decorators and Closures

# Function decorators let us "mark" functions in the source code to enhance their behavior.
# This is powerful stuff, but mastering it requires understanding closures.

# Decorators 101
# A decorator is a callable that takes another function as argument(the decorated function).

def deco(func):
    def inner():
        print('running inner()')
    return inner

@deco
def target():
    print('running target()')

target()

# To summarize:
# The first crucial fact about decorator is that they have the power to replace the decorated function
# with a different one.
# The second crucial fact is that they are executed immediately when a module is loaded.

# When Python executes decorators
# A key feature of decorators is that they run right after the decorated function is defined.
# That is usually at import time.
# The function decorators are executed as soon as the module is imported,
# but the decorated functions only run when they are explicitly invoked.

# To notice:
# 1. A real decorator is usually defined in one module and applied to functions in other modules
# 2. In practice, most decorators define an inner function and return it.

# Decorator-Enhanced Strategy Pattern

# Closures
# Actually, a closure is a function with an extended scope that encompasses nonglobal variables referenced
# in the body of the function but not defined there.
# What matters is that it can access nonglobal variables that are defined outside of its body.

class Averager():
    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total/len(self.series)

avg = Averager()
print(avg(10))
print(avg(12))

def make_averager():
    series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)

    return averager

avg2 = make_averager()
print(avg2(10))
print(avg2(20))

# The nonlocal Declaration
# It lets you flag a variable as a free variable even when it is assigned a new value within the function.

def make_averager2():
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count

    return averager

avg3 = make_averager2()
print(avg3(10))
print(avg3(20))

# Implementing a simple decorator
import time

def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked

@clock
def snooze(seconds):
    time.sleep(seconds)

@clock
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)

print('*' * 40, 'Calling snooze(.123)')
snooze(.123)
print('*' * 40, 'Calling factorial(10)')
print('10! = ', factorial(10))

# Decorators in the Standard Library
# Python has three built-in functions that are designed to decorate methods: property, classmethod, and staticmethod.
# Another frequently seen decorator is functools.wraps, a helper for building well-behaved decorators.

# Memoization with functools.lru_cache
# It implements memoization: an optimization technique that works by saving the results of previous innocations
# of an expensive function, avoiding repeat computations on previously used arguments.
# The letters LRU stand for Least Recently Used.

import functools

@functools.lru_cache()
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

print(fibonacci(6))

# Besides making silly recursive algorithms viable, lru_cache really shines in applications that need to fetch
# information from the Web.

# Generic Functions with Single Dispatch
# Because we don't have method or function overloading in Python, we can't create variations of a function
# with different signatures for each data type we want to handle differently.
# If you decorate a plain function with @singleddispatch, it becomes a generic function: a group of functions
# to perform the same operation in different ways, depending on the type of the first argument.

# Stacked Decorators

# Parameterized Decorators












