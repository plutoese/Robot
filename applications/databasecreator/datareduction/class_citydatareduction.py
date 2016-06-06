# coding=UTF-8

# -----------------------------------------------
# class_citydatareduction文件
# @class: CitydataReduction类
# @introduction: 城市统计年鉴数据预处理方法集合类
# @dependency: winexcel类
# @author: plutoese
# @date: 2016.05.12
# ------------------------------------------------

import re
from libs.file.class_winexcel import WinExcel
from libs.file.class_Excel import Excel
from applications.databasecreator.admindivision.class_admincodefile import AdminCodeFile


class CitydataReduction:
    """ 城市统计年鉴数据预处理方法集合类

    :param list rawdata: 源数据
    :param AdminCodeFile acodefile: 行政代码信息
    :return: 无返回值
    """

    def __init__(self, rawdata=None,acodefile=None):
        self._raw_data = rawdata
        self._acode_file = acodefile

    def reduction(self,parent_limit=1):
        """ 数据清理

        :param parent_limit: 上级层次
        :return: 无返回值
        """
        # 表示数据行是否开始的布尔变量
        is_begin = False
        # 清理后数据存放变量
        self.second_data = []
        # 删除数据存放变量
        self.deleted_data = []
        # 并非全数字变量
        self.not_all_numeric = []
        # 无法关联且并非全数字变量
        self.no_matched_and_not_all_numeric = []
        # 注解数据存放变量
        self.remark = []
        # 表标题数据存放变量
        self.header = []
        # 表单位数据存放变量
        self.unit = []
        # 没有关联到的数据变量
        self.no_matched = []
        # 其他数据变量
        self.others = []
        parent = []
        for row in self._raw_data:
            # 删除空行
            if set(row) == {None}:
                continue
            row0 = re.sub('\s+','',str(row[0]))
            # 匹配标题
            if re.match('^\d(-|—|－)\d+',row0) is not None:
                if len(self.header) > 0:
                    self.deleted_data.append(row)
                    continue
                self.header = [re.sub('(-|—|－)','-',row0)]
                self.second_data.append(self.header)
                continue
            # 匹配单位
            if re.match('^单位',row0) is not None:
                if len(self.unit) > 0:
                    self.deleted_data.append(row)
                    continue
                self.unit = [row0]
                self.second_data.append(self.unit)
                continue
            # 匹配注解
            if re.match('^(\*|①|②|注：|Note)',row0) is not None:
                remark = re.sub('①|②|注：|Note:','*',str(row[0]))
                self.remark.append(remark)
                continue
            # 关联区域名
            region_name = row0
            if len(parent) < 1:
                result = self._acode_file.get_division(region_name)
            else:
                result = self._acode_file.get_division(region_name,parent)
            # 如果匹配成功
            if result is not None:
                rowdata = [row[0],result[-1],result[-2]]
                # 转换数字
                converted_row, sign = self.row_conversion(row[1:])
                rowdata.extend(converted_row)
                if sign:
                    rowdata.append('')
                else:
                    self.not_all_numeric.append(row)
                    rowdata.append('并非全是数字')
                # 根据上级层级，设定上级
                if parent_limit == 1:
                    parent = [result[0]]
                else:
                    if len(result) < 3:
                        parent = [result[0]]
                    else:
                        parent = [result[0],result[1]]
                # 储存数据
                self.second_data.append(rowdata)
                is_begin = True
                continue
            if is_begin:
                if row[0] is None:
                    self.deleted_data.append(row)
                    continue
                #if re.match('^\d+',row0) is not None:
                #    self.deleted_data.append(row)
                #    continue
                if re.match('^城市$',row0) is not None:
                    self.deleted_data.append(row)
                    continue
                if re.match('^续表',row0) is not None:
                    self.deleted_data.append(row)
                    continue
                if re.match('^\(10000(persons|household|tons|kwh)\)',row0) is not None:
                    self.deleted_data.append(row)
                    continue
                if re.match('^\(person(s)?\)',row0) is not None:
                    self.deleted_data.append(row)
                    continue
                if re.match('^\(10000yuan\)',row0) is not None:
                    self.deleted_data.append(row)
                    continue
                if re.match('^\((unit|ton|household)\)',row0) is not None:
                    self.deleted_data.append(row)
                    continue
                if re.match('^\(\%\)$',row0) is not None:
                    self.deleted_data.append(row)
                    continue
                if re.match('^\%$',row0) is not None:
                    self.deleted_data.append(row)
                    continue
                rowdata = [row[0],'','']
                converted_row, sign = self.row_conversion(row[1:])
                rowdata.extend(converted_row)
                if sign:
                    self.no_matched.append(row)
                    rowdata.append('没找到对应的行政区划')
                else:
                    self.no_matched_and_not_all_numeric.append(row)
                    rowdata.append('没找到对应的行政区划且并非全是数字')
                self.second_data.append(rowdata)
                continue
            rowdata = list(row)
            rowdata.insert(1,'')
            rowdata.insert(1,'')
            self.others.append(row)
            self.second_data.append(rowdata)
        if len(self.remark) > 0:
            self.second_data.append(self.remark)

    @staticmethod
    def row_conversion(rowdata,to='float'):
        all = True
        new_row = []
        for item in rowdata:
            if item is None:
                continue
            new_item = re.sub('\s+','',str(item))
            if len(new_item) < 1:
                continue
            if re.match('^-$',new_item) is not None:
                continue
            if re.match('^(-)?\d+((\.|．)\d+)?$',new_item) is not None:
                new_item = re.sub('．','.',new_item)
                new_row.append(float(new_item))
            else:
                all = False
                new_row.append(item)
        return new_row,all

if __name__ == '__main__':
    filename = r'E:\data\procedure\Process\reduction\data\admincode\2003.xls'
    acodefile = AdminCodeFile(filename)

    filename = r'E:\data\procedure\Process\reduction\data\2003_prefecture\3_3_按三次业人员就业状况_地级市_2003.xls'
    mexcel = WinExcel(filename)
    mdata = mexcel.read()
    reduction = CitydataReduction(mdata,acodefile)

    reduction.reduction()
    ndata = reduction.second_data
    print(reduction.second_data)

    outfile = r'd:\data\demo.xlsx'
    moutexcel = Excel(outfile)
    moutexcel.new().append(ndata, 'mysheet')
    moutexcel.close()





