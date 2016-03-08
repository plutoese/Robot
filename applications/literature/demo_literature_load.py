# coding=UTF-8

import json

literatures = json.load(open(r'E:\gitrobot\files\literature\literature_list.txt'))
for liter in literatures:
    print(liter)
    print(literatures[liter])
