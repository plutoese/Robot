# coding=UTF-8

# Fluent Python
# Chapter 4: Text versus Bytes

# Character Issues
# The Unicode standard explicitly seperates the identity of characters from specific byte representations.
# The identity of a character - its code point - is a number from 0 to 1114111, shown in the Unicode
# standard as 4 to 6 hexadecimal digits with a "U+" prefix. For example, the code point for the letter A
# is U+0041.
# The actual bytes that represent a character depend on the encoding in use. An encoding is an algorithm
# that converts code point to byte sequences and vice versa. The code point for A (U+0041) is encoded as
# the single byte \x41 in the UTF-8 encoding.

# Converting from code point to bytes is encoding; converting from bytes to code points is decoding.
s = 'café'
print(len(s))
b = s.encode('utf-8')
print(len(b))
s1 = b.decode('utf-8')
print(s1)

# There are two basic built-in types for binary sequences: the immutable bytes type and the mutable bytearray.
# Each item in bytes or bytearray is an integer from 0 to 255.
cafe = bytes('café',encoding='utf-8')
print(cafe)
print(cafe[0],cafe[0:1])
cafe_arr = bytearray(cafe)
print(cafe_arr)
print(cafe_arr[-1:])

# The regular expression functions in the re module work on binary sequences.

# Basic Encoders/Decoders
# The Python distribution bundles more than 100 codes(encoder/decoder) for text to byte conversion
# and vice versa.
# Each codec has a name, like 'utf_8', and often aliases, such as 'utf8', 'utf-8', and 'U8', which
# you can use as the encoding argument in functions like open(), str.encode(), bytes.decode(), and so on.

# Understanding Encode/Decode Problems
# Coping with UnicodeEncodeError
# Most non-UTF codecs handle only a small subset of the Unicode characters.
# When converting text to bytes, if a character is not defined in the target encoding, UnicodeEncodeError
# will be raised.

# Coping with UnicodeDecodeError
# Not every bytes holds a valid ASCII character, and not every byte sequence is valid UTF-8 or UTF-16.

# SyntaxError when loading modules with Unexpected Encoding
# If you load a.py module containing non-UTF-8 data and no encoding declaration, you would get this message.
# Because UTF-8 is widely deployed in GNU/Linux and OSX systems, a likely scenario is opening a.py file
# created on Windows with cp1252. Note that this error happens even in Python for Windows, because
# the default encoding for Python 3 is UTF-8 across all platforms.
# To fix this problem, add a magic coding comment at the top of the file. like this
# coding: cp1252

# How to discover the Encoding of a Byte Sequence
# How do you find the encoding of a byte sequence? Short answer: you can't. You must be told.
# Chardet is a Python library that you can use in your programs, but also inculdes a command-line
# utility, chardetect.

# Handling Text Files
# The best practice for handling text is the "Unicode sandwich". This means that bytes should be
# decoded to str as early as possible on input. The 'meat' of the sandwich is the business logic
# of your program, where text handling is done exclusively on str objects.
# You should never be encoding or decoding in the middle of other processing.
# On output, the str are encoded to bytes as late as possble.

import os

fp = open('d:/down/cafe.txt','w',encoding='utf-8')
print(fp)
fp.write('café')
fp.close()

fp2 = open('d:/down/cafe.txt')
print(fp2)
print(os.stat('d:/down/cafe.txt').st_size)
print(fp2.encoding)
print(fp2.read())

fp3 = open('d:/down/cafe.txt',encoding='utf-8')
print(fp3)
print(fp3.read())
print('done!')

fp4 = open('d:/down/cafe.txt','rb')
print(fp4)
text4 = fp4.read()
print(text4)
print(text4.decode(encoding='utf-8'))






