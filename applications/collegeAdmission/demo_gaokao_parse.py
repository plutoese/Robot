# coding=UTF-8

import pickle
import re

fp = open(r'E:\gitrobot\files\college\exam\college_list.pkl','rb')
colleges_list = pickle.load(fp)

vars = ['university','student_region','subject','year','batch','average_score','province_control_score']
colleges = []
for cstr in colleges_list:
    for item in re.split('\n',cstr)[1:]:
        colleges.append(dict(zip(vars,re.split('\s+',item)[0:8])))

for item in colleges:
    if re.match('^--$',item['average_score']) is not None:
        item['average_score'] = None
    else:
        item['average_score'] = int(item['average_score'])
    if re.match('^--$',item['province_control_score']) is not None:
        item['province_control_score'] = None
    else:
        item['province_control_score'] = int(item['province_control_score'])

for item in colleges:
    print(item)

