# coding=UTF-8

import pandas as pd
import numpy as np
from libs.database.class_cgssdatabase import CgssDatabase
from libs.file.class_Excel import Excel

filename = r'D:\data\student.xls'
Path = r'D:\data\labdata'
mexcel = Excel(filename)
mdata = mexcel.read()
mdata = [item[1] for item in mdata]

cgdb = CgssDatabase(year=2013)
pdata = cgdb.variables(variables=[['a2', False], ['a3a', False],
                                  ['a4', False],['a7a', False],
                                  ['a8a', False],['a8b', False],
                                  ['a10', False],['a18', False],
                                  ['a59j',False],['a69',False],['a89b',False]])
pdata.columns = ['A10政治面貌','A18户口登记状况',
                 'A2性别','A3a出生年份','A4民族','A59j前工作的单位或公司的单位类型',
                 'A69婚姻状况',
                 'A7a目前的最高教育程度','A89b父亲的最高教育程度',
                 'A8a个人去年全年的总收入','A8b个人去年全年的职业（劳动）收入'
                 ]

for sname in mdata:
    index = np.random.choice(11436,1000,replace=False)
    mdata = pdata.ix[index]
    mdata.to_excel(''.join([Path,'\\',sname,'.xls']),index=False)





