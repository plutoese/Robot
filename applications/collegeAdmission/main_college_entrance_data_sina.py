# coding=UTF-8

import random
import json
from libs.file.class_Excel import Excel
from applications.collegeAdmission.class_ceespidersina import CEESpiderSina

# 0. Initial configuration
valid_proxy = ['61.174.10.22:8080', '101.66.253.22:8080','61.174.13.12:80', '101.200.178.46:3128','101.226.249.237:80']

regions = ['北京','天津','上海','重庆','河北','河南','山东','山西','安徽','江西',
           '江苏','浙江','湖北','湖南','广东','广西','云南','贵州','四川','陕西',
           '青海','宁夏','黑龙江','吉林','辽宁','西藏','新疆','内蒙古','海南','福建',
           '甘肃']
subject = ['文科','理科']
year = ['2014','2013','2012','2011','2010','2009','2008']
batch = ['本科一批','本科二批','本科三批']


result = []


YEAR = year[0]
BATCH = batch[0]

# 1. 开始抓取Z
spider = CEESpiderSina(proxy=valid_proxy[random.randint(0,len(valid_proxy)-1)])
for region in regions[20:]:
    print(region)
    for sub in subject:
        spider.clear()
        print(sub)

        spider.select_region(region)
        spider.select_subject(sub)
        spider.select_year(YEAR)
        spider.select_batch(BATCH)
        spider.do_search()
        spider.get_result_and_more()

        file_name = ''.join(['E:/robot/files/college/exam/',region,'_',sub,'_',YEAR,'_',BATCH,'.txt'])
        json.dump(spider.colleges, fp=open(file_name,'w'))

spider.close()

'''
file = ''.join(['E:/robot/files/college/exam/','北京_理科_2014_本科一批','.txt'])
F = json.load(fp=open(file,'r'))
for item in F:
    print(item)
print(len(F))'''