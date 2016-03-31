# coding=UTF-8

import re
from libs.file.class_Excel import Excel
from libs.database.class_mongodb import MongoDB

# 0. 导入Mongodb
db = MongoDB()
db.connect('publication','ChineseJournal')

# 1. 载入publication文件
CHINESE_JOURNAL = 'E:\\gitrobot\\files\\publication\\Chinese_journal.xlsx'

mexcel = Excel(CHINESE_JOURNAL)
jouranls_economics = mexcel.read(sheet='社会科学')

variables = jouranls_economics[0][1:5]
print('variable',variables)

'''
for item in jouranls_economics[1:]:
    old_record = item[1:5]
    if isinstance(old_record[2],str):
        continue
    old_record[0] = re.sub('\s+','',old_record[0])
    old_record[1] = re.sub('\s+','',old_record[1])
    record = dict(zip(variables,old_record))
    print(record)
    db.collection.insert_one(record)

'''
item = ['中国人口·资源与环境','中国可持续发展研究会;山东省可持续发展研究中心;中国21世纪议程管理中心;山东师范大学',2.802,1.779]
record = dict(zip(variables,item))
print(record)
#db.collection.insert_one(record)