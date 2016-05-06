# coding=UTF-8

import re
import json
from libs.file.class_Excel import Excel
from libs.database.class_mongodb import MongoDB

'''
# 0. read impact file
Impact_File = 'E:\\gitrobot\\files\\publication\\Western_journal.xlsx'
impact_factor = Excel(Impact_File).read(sheet=4)
impact_factor_journals = dict()
for item in impact_factor[1:]:
    if item[2] > 0:
        impact_factor_journals[item[1]] = item[2]

# 1. read ssci file
result = []
journals = json.load(open(r'E:\gitrobot\files\publication\ssci_geography_json.txt'))
for journal in journals:
    if journal[1] not in impact_factor_journals:
        result.append([journal[0].upper(),journal[1],None])
    else:
        result.append([journal[0].upper(),journal[1],impact_factor_journals[journal[1]]])

# 2. output
for record in result:
    print(record)

outfile = r'd:\down\tmp_journal.xlsx'
moutexcel = Excel(outfile)
moutexcel.new().append(result, 'sheet1')
moutexcel.close()'''

mongo = MongoDB()
mongo.connect('publication','WesternJournal')
filename = r'd:\down\journals.xlsx'
mexcel = Excel(filename)
mdata = mexcel.read(sheet=4)
result = []
for item in mdata[1:]:
    if item[2] == '':
        result.append({'journal':item[0],'SSIN':item[1],'IF':None})
    else:
        result.append({'journal':item[0],'SSIN':item[1],'IF':item[2]})

#for j in result:
#    mongo.collection.insert_one(j)