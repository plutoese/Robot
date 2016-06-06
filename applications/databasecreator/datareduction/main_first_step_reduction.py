# coding=UTF-8

import re
import os
from libs.file.class_winexcel import WinExcel
from libs.file.class_Excel import Excel
from applications.databasecreator.admindivision.class_admincodefile import AdminCodeFile
from applications.databasecreator.datareduction.class_citydatareduction import CitydataReduction

# 0.参数设置
# 0.1 全局参数设置
IMPORT_PATH = r'E:\data\procedure\Process\reduction\data'
EXPORT_PATH = r'E:\data\procedure\Process\reduction\first_step_data'
ADMINCODE_PATH = r'E:\data\procedure\Process\reduction\data\admincode'
ENGLISH = False

# 0.2 变参数设置
year = '1994'
current_work_dir = '1994_prefecture'

# 0.3 创建当前工作目录
current_import_dir = os.path.join(IMPORT_PATH,current_work_dir)

# 0.4 创建文件导出的目录
current_export_path = os.path.join(EXPORT_PATH,current_work_dir)
if not os.path.exists(current_export_path):
    os.mkdir(current_export_path)

# 1. 导入行政区划代码文件，创建AdminCodeFile对象
admin_code_file = os.path.join(ADMINCODE_PATH,''.join([year,'.xls']))
acodefile = AdminCodeFile(admin_code_file)

# 2. 转换工作
for file in os.listdir(current_import_dir):
    print(file)
    abnormal = False
    if '&' in file:
        abnormal = True
        region_col = int(re.split('\.',re.split('&',file)[1])[0])
    # 源文件
    source_file = os.path.join(current_import_dir,file)
    # 目标文件
    file_name = re.split('\.',file)[0]
    new_file_name = ''.join([file_name,'_first_step.xlsx'])
    new_delete_name = ''.join([file_name,'_deleted.xlsx'])
    target_file = os.path.join(current_export_path,new_file_name)
    delete_file = os.path.join(current_export_path,new_delete_name)

    # 如果目标文件存在，那么跳过
    if os.path.exists(target_file):
        print('Here it is! ',file)
        continue

    # 从excel文件读入数据，构建CitydataReduction对象
    #mexcel = WinExcel(source_file)
    mexcel = Excel(source_file)
    sdata = mexcel.read()
    if abnormal:
        ndata = []
        first_part = []
        second_part = []
        for row in sdata:
            if set(row) == {None}:
                if len(first_part) < 1:
                    continue
                else:
                    ndata.extend(first_part)
                    ndata.extend(second_part)
                    first_part = []
                    second_part = []
            first_part.append(row[0:region_col])
            second_part.append(row[region_col:])
        sdata = ndata
    #mexcel.close()

    if ENGLISH:
        ndata = []
        for item in sdata:
            first = [item[0]]
            first.extend(item[2:])
            ndata.append(first)
        sdata = ndata
    reduction = CitydataReduction(sdata,acodefile)

    # 进行数据整理
    reduction.reduction()
    # 得到整理完的数据
    ndata = reduction.second_data

    # 输出相关信息
    print('-'*30)
    if len(reduction.header) < 1:
        print('标题: ','没有')
    else:
        print('标题: ',reduction.header[0])
    print('Number of Rows: ',len(reduction.second_data))
    for item in reduction.no_matched:
        print('Not Matched: ',item)
    for item in reduction.not_all_numeric:
        print('Not All Numeric: ',item)
    for item in reduction.no_matched_and_not_all_numeric:
        print('Not Matched and Not All Numeric: ',item)
    #for item in reduction.deleted_data:
    #    print('Deleted Row: ',item)
    for item in reduction.remark:
        print('Remark: ',item)
    for item in reduction.others:
        print('Others: ',item)
    print('*'*30)

    moutexcel = Excel(target_file)
    moutexcel.new().append(ndata, 'sheet')
    moutexcel.close()

    '''
    moutexcel2 = Excel(delete_file)
    moutexcel2.new().append(reduction.deleted_data, 'sheet')
    moutexcel2.close()'''



