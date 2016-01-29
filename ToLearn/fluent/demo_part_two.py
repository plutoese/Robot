# coding=UTF-8

# Theme: Function
# Author: glen
# Date: 2016.1.27

# 1. First-Class Functions
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)

print(factorial(10))
print(type(factorial))

fact = factorial
print(fact(6))

print(list(map(fact, range(11))))

# Higher-Order Functions






