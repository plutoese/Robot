# coding=UTF-8

# --------------------------------------------------------------
# class_Path文件
# @class: Path
# @introduction: Path类用来处理文件夹
# @dependency: os, os.path包
# @author: plutoese
# @date: 2016.01.28
# --------------------------------------------------------------

import os
import re
from libs.file.class_pathparse import PathParse
import shutil

class PathNew:
    """Path类用来处理文件夹

    """
    def __init__(self, full_path, base_path=None):
        # 调用PathParse类对目录名进行解析
        self.parse = PathParse(full_path)
        # 如果full_path是目录，继续进行；否则就报错
        if os.path.isdir(full_path):
            # self.__full_path是完整目录
            self.__full_path = full_path
            # self.__parent_path是父目录
            # self.__path是当前目录
            self.__parent_path, self.__path = os.path.split(self.__full_path)
        else:
            print('{} is not a directory!'.format(full_path))
            raise FileNotFoundError

        # 设定self.__base_path，是为了获得相对目录
        self.__base_path = base_path
        self.__relative_path = None
        # 设置相对目录，和相对父目录
        if base_path is not None:
            if os.path.isdir(base_path):
                self.__relative_path = os.path.relpath(self.__full_path,self.__base_path)
                self.__relative_parent_path = os.path.relpath(self.__parent_path,self.__base_path)
            else:
                print('{} is not a directory!'.format(base_path))
                raise FileNotFoundError

    # 这个方法用来打印目录下所有子目录和文件
    def walk_and_record(self):
        self.__path_included = []
        for path in os.walk(self.__full_path):
            print(path)

    def find(self,keyword):
        if isinstance(keyword,str):
            return self.find_by_string(keyword)
        else:
            return self.find_by_list(keyword)

    # 通过字符串寻找路径
    def find_by_string(self,piece):
        """寻找目录

        :param str piece: 目录关键字
        :return:
        """
        for item in os.walk(self.__full_path):
            if re.match(os.path.split(item[0])[1],piece) is not None:
                return os.path.normpath(item[0])
        return None

    # 通过字符串列表寻找路径
    def find_by_list(self,pieces):
        """寻找目录

        :param list pieces: 目录关键字
        :return:
        """
        base_path = self.__full_path
        for piece in pieces:
            for item in os.walk(base_path):
                 if re.match(os.path.split(item[0])[1],piece) is not None:
                    base_path = item[0]
                    continue
        if base_path == self.__full_path:
            return None
        else:
            return base_path

    # 压缩目录为zip文件，并且返回zip文件的完整目录
    def compress(self):
        """压缩目录为zip文件

        :return:
        """
        #zip_file_name = ''.join([self.parse.file_name_with_dir,'.zip'])
        shutil.make_archive(self.parse.file_name_with_dir,'zip',self.__full_path,'.')
        return os.path.normpath(''.join([self.parse.file_name_with_dir,'.zip']))

    def append_file_suffix(self,suffix=None):
        """添加后缀到目录下的所有文件

        :param suffix:
        :return:
        """
        for item in os.walk(self.__full_path):
            [os.rename(''.join([item[0],'\\',filename]),
                       ''.join([item[0],'\\',PathParse(''.join([item[0],'\\',filename])).file_name_without_extension,suffix,'.',PathParse(''.join([item[0],'\\',filename])).extension]))
             for filename in item[2]]

    def is_child_of(self,parent_path):
        if not os.path.isdir(parent_path):
            print('{} is not a valid path.'.format(parent_path))
            raise TypeError
        else:
            normal_parent_path = os.path.normpath(parent_path)
            normal_path = os.path.split(os.path.normpath(self.full_path))[0]
            if normal_parent_path == normal_path:
                return True
            else:
                return False

    def is_have_special_symbol(self,special_symbol='@#$%&{='):
        path_set = set(self.path)
        for item in special_symbol:
            if item in path_set:
                return True
        return False


    @property
    def full_path(self):
        return os.path.normpath(self.__full_path)

    @property
    def path(self):
        return os.path.normpath(self.__path)

    @property
    def parent_path(self):
        return os.path.normpath(self.__parent_path)

    @property
    def relative_path(self):
        return os.path.normpath(self.__relative_path)

    @property
    def relative_parent_path(self):
        return os.path.normpath(self.__relative_parent_path)

    @property
    def included(self):
        return os.walk(self.__full_path)

if __name__ == '__main__':
    file_path = Path('E:\\piles\\temp','E:\\')
    file_path.walk_and_record()
    print(file_path.full_path)
    print(file_path.path)
    print(file_path.parent_path)
    print('-----------------------')
    print(file_path.relative_path)
    print(file_path.relative_parent_path)
    print(file_path.included)
    print('***********************')
    print(file_path.find(['yadong','yes']))
    print('newssssssssssss',os.path.isfile(file_path.compress()))
    #file_path.append_file_suffix('@glen#2012%database%mongodb%test')
    print('^^^^^^^^^^^^^^^^^^^^^^^^^')
    print(file_path.is_child_of('E:/room'))
    file_path2 = Path(r'E:\room\forawhile\personalnote@glen#2012%note&researchproject')
    #file_path2 = Path(r'E:\room\forawhile\选课手册导出@glen#2012%database%mongodb%test   blank{自科基金{社科基金=')
    print(file_path2.path)
    print(file_path2.is_have_special_symbol())








