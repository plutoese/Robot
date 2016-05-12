# coding=UTF-8

import os.path
import re
from collections import OrderedDict
from libs.file.class_Excel import Excel

# 0. To set up
YEAR1 = 2000
YEAR2 = 2013

# 1. To read data from admincode
admin_file = ''.join(['E:\\data\\admincode\\',str(YEAR1),'.xls'])
#admin_file = ''.join(['E:\\data\\admincode\\',str(YEAR2),'.xls'])
admin_data = Excel(admin_file).read()
region_list = [re.sub('\s+','',item[1]) for item in admin_data[1:]]
admin_code = OrderedDict([(re.sub('\s+','',item[1]),str(int(item[0]))) for item in admin_data[1:]])
print(admin_code)

# 2. To read data from data_file
excel_data = Excel(r'E:\data\dbproject\testdata.xls').read()
#excel_data = Excel(r'E:\data\dbproject\testdata2.xls').read()
region_to_match = [re.sub('\s+','',item[0]) for item in excel_data]
print(region_to_match)

# 3. 匹配
for region in region_to_match:
    if region in admin_code:
        print(region,' --: ',admin_code[region])
    else:
        print(region,' not matched!')