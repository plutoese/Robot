# coding=UTF-8

# -----------------------------------------------
# class_admincodefile文件
# @class: AdminCodeFile类
# @introduction: AdminCodeFile类用来提取民政部的行政代码信息
# @dependency: xlrd
# @author: plutoese
# @date: 2016.05.12
# ------------------------------------------------

from libs.file.class_Excel import Excel
from collections import OrderedDict
import re

class AdminCodeFile:
    """ AdminCode类用来提取民政部的行政代码信息

    :param str filename: 想要读写的文件名
    :return: 无返回值
    :var str filename: 文件名
    """

    def __init__(self, file_name=None):
        mexcel = Excel(file_name)
        self._raw_acode_data = mexcel.read()

        self.region_list = [re.sub('\s+','',item[1]) for item in self._raw_acode_data[1:]]
        self.admin_code_dict = OrderedDict([(re.sub('\s+','',item[1]),str(int(item[0]))) for item in self._raw_acode_data[1:]])
        self.code_admin_dict = OrderedDict([(str(int(item[0])),re.sub('\s+','',item[1])) for item in self._raw_acode_data[1:]])

        self._create_relationship()

    def get_division(self,name,parent=None):
        if parent is None:
            # 省级寻找
            for rname in self.second_level_division_dict:
                if re.match(name,rname) is not None:
                    return self.second_level_division_dict[rname],rname
            # 地级寻找
            for rname in self.third_level_division_dict:
                if re.match(name,rname) is not None:
                    parent_acode = ''.join([self.third_level_division_dict[rname][0:2],'0000'])
                    if parent_acode in self.second_level_division:
                        return parent_acode,self.third_level_division_dict[rname],rname
                    else:
                        print('Parent not found!!')
            # 县级寻找
            for rname in self.fourth_level_division_dict:
                if re.match(name,rname) is not None:
                    parent_acode = ''.join([self.fourth_level_division_dict[rname][0:4],'00'])
                    if parent_acode in self.third_level_division:
                        grandpa_code = ''.join([parent_acode[0:2],'0000'])
                        if grandpa_code in self.second_level_division:
                            return grandpa_code,parent_acode,self.fourth_level_division_dict[rname],rname
                        else:
                            print('Grandpa not found!!')
                    else:
                        parent_acode = ''.join([self.fourth_level_division_dict[rname][0:2],'0000'])
                        if parent_acode in self.second_level_division:
                            return parent_acode,self.fourth_level_division_dict[rname],rname
                        else:
                            print('Parent not found!!')
            return None
        else:
            if len(parent) < 2:
                children = self.second_children[parent[0]]
                children_dict = dict([(self.code_admin_dict[code],code) for code in children])
                for rname in children_dict:
                    if re.match(name,rname) is not None:
                        return parent[0],children_dict[rname],rname
            elif len(parent) < 3:
                children = self.third_children[parent[1]]
                children_dict = dict([(self.code_admin_dict[code],code) for code in children])
                for rname in children_dict:
                    if re.match(name,rname) is not None:
                        return parent[0],parent[1],children_dict[rname],rname
            else:
                print('Too much parents!!!')

            result = self.get_division(name)
            return result

    def _create_relationship(self):
        # 二级行政区划，省级
        self.second_level_division = set([item for item in self.code_admin_dict.keys()
                                          if re.match('^\d{2}0000$',item) is not None])
        self.second_level_division_dict = dict([(self.code_admin_dict[acode],acode) for acode in self.second_level_division])

        third_level_division = set([item for item in self.code_admin_dict.keys() if re.match('^\d{4}00$',item) is not None])
        # 三级行政区划，地级
        self.third_level_division = third_level_division - self.second_level_division
        # 四级行政区划，地级
        self.fourth_level_division = set(self.code_admin_dict.keys()) - self.second_level_division - self.third_level_division

        self.third_level_division_dict = dict([(self.code_admin_dict[acode],acode) for acode in self.third_level_division])
        self.fourth_level_division_dict = dict([(self.code_admin_dict[acode],acode) for acode in self.fourth_level_division])

        # 省级行政区划下属
        self.second_children = dict()
        for item in self.second_level_division:
            self.second_children[item] = [unit for unit in self.third_level_division
                                          if item[0:2] == unit[0:2]]
        # 地级行政区划下属
        self.third_children = dict()
        for item in self.third_level_division:
            self.third_children[item] = [unit for unit in self.fourth_level_division
                                         if item[0:4] == unit[0:4]]

        fourth_division_done = []
        for k in self.third_children:
            fourth_division_done.extend(self.third_children[k])
        fourth_division_left = self.fourth_level_division - set(fourth_division_done)

        for item in fourth_division_left:
            found = False
            for s in self.second_children:
                if s[0:2] == item[0:2]:
                    self.second_children[s].append(item)
                    found = True
                    continue
            if not found:
                print('IIIIIIIIIIIIIIIII')


if __name__ == '__main__':
    filename = r'E:\data\procedure\Process\reduction\data\admincode\1999.xls'
    acodefile = AdminCodeFile(filename)
    print(acodefile._raw_acode_data)
    print(acodefile.region_list)
    print(acodefile.admin_code_dict)
    print(acodefile.code_admin_dict)

    print(acodefile.third_level_division)
    print(len(acodefile.third_level_division))
    print(acodefile.third_children)

    print(acodefile.get_division('石家庄',parent=['130000', '130500']))
    print(acodefile.get_division('克垃玛依'))
