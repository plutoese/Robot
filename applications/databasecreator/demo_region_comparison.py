# coding=UTF-8

import os.path
from libs.file.class_Excel import Excel

# 0. To set up
YEAR = 1999
BASE_PATH = 'E:\\data\\中国城市统计年鉴_姚心怡\\'

# 1. To read data from admincode
admin_file = ''.join(['E:\\data\\admincode\\',str(YEAR),'.xls'])
admin_data = Excel(admin_file).read()
region_list = [item[1] for item in admin_data[1:]]
admin_code = dict([(item[1],str(int(item[0]))) for item in admin_data[1:]])
print(region_list)

# 2. To read data from data_file
prefecture_relative_dir = ''.join([str(YEAR),'年地级市','\\'])
prefecture_abs_dir = ''.join([BASE_PATH,prefecture_relative_dir])
county_relative_dir = ''.join([str(YEAR),'年县级','\\'])
county_abs_dir = ''.join([BASE_PATH,county_relative_dir])

print(''.join([prefecture_abs_dir,os.listdir(prefecture_abs_dir)[0]]))
data = Excel(''.join([prefecture_abs_dir,os.listdir(prefecture_abs_dir)[0]])).read()
print(data)











