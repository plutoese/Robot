# coding=UTF-8

import os.path
import json

# 1. setup
PATH = 'E:\\Room\\Library\\dataadministrator\\specialdata\\college entrance\\001 北京大学\\'
FILES = os.listdir(PATH)
print(FILES)
college_files = [''.join([PATH,item]) for item in FILES]

for file in college_files:
    F = json.load(fp=open(file,'r'))
    for d in F:
        print(d['student_region'],' ; ',d['year'],'==',d['subject'],' --- ',d['average_score'],' --- ',d['province_control_score'])

    print('***************************************************')


'''
file = ''.join(['E:/gitrobot/files/college/exam/','北京大学','.txt'])
F = json.load(fp=open(file,'r'))
for item in F:
    print(item)
print(len(F))'''

