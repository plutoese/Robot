# coding=UTF-8

import json
from libs.file.class_Excel import Excel
from libs.database.class_mongodb import MongoDB

mongo = MongoDB()
mongo.connect('college','collegeinfo')

filename = r'E:\data\college\college_rating.xlsx'
'''
colleges = []
vars = ['rating','name','region','type','score']
college_data_2014 = Excel(file_name=filename).read('2014')
for item in college_data_2014[2:]:
    colleges.append(dict(zip(vars,item[0:5])))
print(colleges)

mongo = MongoDB()
mongo.connect('college','collegeinfo')
for item in colleges:
    mongo.collection.insert_one(item)'''

colleges_985 = Excel(file_name=filename).read('985')
for item in colleges_985:
    result = mongo.collection.find_one({'name':item[0]})
    if result is not None:
        mongo.collection.update_one({'name'})
