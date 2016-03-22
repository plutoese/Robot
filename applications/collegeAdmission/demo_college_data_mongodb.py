# coding=UTF-8

import json
import re
from libs.file.class_Excel import Excel
from libs.database.class_mongodb import MongoDB
import os.path

mongo = MongoDB()
mongo.connect('region','province')

filename_college = r'E:\data\college\college_rating.xlsx'
filename_province = r'E:\data\college\province.xlsx'

college_rating = Excel(file_name=filename_college)
province = Excel(file_name=filename_province)

province_dict = dict([(item['region'],item['acode']) for item in mongo.collection.find({})])

def to_acode(province_dict,regions):
    if isinstance(regions,str):
        if '/' in regions:
            regions = re.split('/',regions)
        else:
            regions = [regions]

    result = []
    found = False
    all_found = 0
    for region in regions:
        for province in province_dict:
            if re.match(region,province) is not None:
                all_found += 1
                result.append(province_dict[province])
    if all_found == len(regions):
        found = True
    return (found,result)

'''
colleges = []
vars = ['rating','name','region','type','score']
college_data_2014 = college_rating.read('2014')
for item in college_data_2014[2:]:
    one_item = dict(zip(vars,item[0:5]))
    one_item['rating'] = int(one_item['rating'])
    found,acode = to_acode(province_dict,item[2])
    one_item['region'] = acode
    one_item['project'] = []
    if not found:
        print('*************Not Found************',one_item['region'])
    if len(one_item) < 5:
        print('NOT GOOD ONE',one_item)
    colleges.append(one_item)
print(colleges)

mongo = MongoDB()
mongo.connect('college','collegeinfo')
for item in colleges:
    mongo.collection.insert_one(item)

mongo.connect('college','collegeinfo')
colleges_985 = Excel(file_name=filename_college).read('985')
for item in colleges_985:
    result = mongo.collection.find_one({'name':item[0]})
    if result is not None:
        print('hello')
        mongo.collection.find_one_and_update({'name':item[0]},{'$addToSet':{'project':'985'}})
    else:
        print('---------------',item)

mongo.connect('college','collegeinfo')
colleges_211 = Excel(file_name=filename_college).read('211')
for item in colleges_211:
    result = mongo.collection.find_one({'name':item[0]})
    if result is not None:
        print('hello')
        mongo.collection.find_one_and_update({'name':item[0]},{'$addToSet':{'project':'211'}})
    else:
        print('---------------',item)'''
'''
mongo.connect('college','collegeinfo')
mongo2 = MongoDB()
mongo2.connect('college','entranceexam')
PATH = 'E:\\data\\college\\2014\\'
for file in os.listdir(PATH):
    file_name = ''.join([PATH,file])
    records = json.load(fp=open(file_name,'r'))
    for record in records:
        found_student, [student_region] = to_acode(province_dict,record['student_region'])
        found_unversity, [university_region] = to_acode(province_dict,record['university_region'])
        if not found_student:
            print('WRONG STUDENT',record['student_region'])
            raise FileNotFoundError
        if not found_unversity:
            print('WRONG UNIVERSITY',record['university_region'])
            raise FileNotFoundError

        college = mongo.collection.find_one({'name':record['university']})
        if college is not None:
            record['student_region'] = student_region
            record['university_region'] = university_region
            record['average_score'] = int(record['average_score'])
            mongo2.collection.insert_one(record)
            #print('RECORD',record)
        else:
            print('NOT FOUND ',record['university'])
'''

mongo2 = MongoDB()
mongo2.connect('college','entranceexam')
print(len(list(mongo2.collection.find({}))))