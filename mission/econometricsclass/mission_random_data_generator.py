# coding=UTF-8

import numpy as np
import pandas as pd
from libs.file.class_Excel import Excel

# 0. 导入学生名单
STUDENT_FILE = 'E:\\temp\\lab\\student.xls'
mexcel = Excel(STUDENT_FILE)
student_list = mexcel.read()
students = [item[1] for item in student_list]

# 1. 生成学生数据和答案
out_path = 'E:\\temp\\lab\\'
file_name = '_data.xls'
rules1 = [1,2,4]
rules3 = [3,7,9]
result = [['student','model1','','','','model2','','','','model3','','','','model4','','','']]
for student in students:
    mu, sigma = 0, np.random.randint(1,20)/10
    miu = np.random.normal(mu, sigma, 1000)

    x1 = np.random.randint(1,100,1000)
    x2 = 5 + np.random.randint(1,5)*x1/10 + np.random.normal(mu, 0.1, 1000)
    x3 = np.random.randint(1,200,1000)

    pdata = pd.DataFrame({'x1':x1,'x2':x2,'x3':x3})
    one_student_coefs = [student]
    for i in range(0,4):
        constant = np.random.randint(1,100,1)
        coefs = np.random.randint(0,10,3)

        print('coefs',coefs[0],coefs[0] in rules1)

        full_coefs = list(constant)
        full_coefs.extend(list(coefs))
        one_student_coefs.extend(full_coefs)

        y = constant + coefs[1]*x2 + miu
        if coefs[0] in rules1:
            y += coefs[0]*np.log(x1)
        else:
            y += coefs[0]*x1
        if coefs[2] in rules3:
            y += coefs[2]*np.log(x3)
        else:
            y += coefs[2]*x3

        pdata[''.join(['y',str(i+1)])] = y
    result.append(one_student_coefs)

    pdata.to_excel(excel_writer = ''.join([out_path,student,file_name]),index=False)

print(result)
out_path = 'E:\\temp\\lab\\result.xlsx'
mexcel = Excel(out_path)
mexcel.new().append(result)
mexcel.close()


'''
# 1. 正态分布的随机数
mu, sigma = 0, 1
s = np.random.normal(mu, sigma, 1000)
print(abs(mu - np.mean(s)) < 0.1, np.mean(s))

# 2. 生成数学表达式
x1 = np.random.randint(0,100,1000)
print(np.mean(x1))
y = 2 + 3*x1 + s
print(np.mean(y))

mdata = pd.DataFrame({'x1':x1,'y':y})
print(mdata)

# 3. 导出数据到Excel文件
out_path = 'E:\\temp\\lab\\'
file_name = 'data.xls'

mdata.to_excel(excel_writer = ''.join([out_path,file_name]))'''













