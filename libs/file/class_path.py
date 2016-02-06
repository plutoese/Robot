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

class Path:
    """Path类用来处理文件夹

    """
    def __init__(self, full_path, base_path=None):

        self.parse = PathParse(full_path)

        if os.path.isdir(full_path):
            self.__full_path = full_path
            self.__parent_path, self.__path = os.path.split(self.__full_path)
        else:
            print('{} is not a directory!'.format(full_path))
            raise FileNotFoundError

        self.__base_path = base_path
        self.__relative_path = None
        if base_path is not None:
            if os.path.isdir(base_path):
                self.__relative_path = os.path.relpath(self.__full_path,self.__base_path)
                self.__relative_parent_path = os.path.relpath(self.__parent_path,self.__base_path)
            else:
                print('{} is not a directory!'.format(base_path))
                raise FileNotFoundError


    def walk_and_record(self):
        self.__path_included = []
        for path in os.walk(self.__full_path):
            print(path)

    def find(self,piece):
        """寻找目录

        :param str piece: 目录关键字
        :return:
        """
        for item in os.walk(self.__full_path):
            if re.search(os.path.split(item[0])[1],piece) is not None:
                return item[0]
        return None

    def compress(self):
        """压缩目录为zip文件

        :return:
        """
        zip_file_name = ''.join([self.parse.file_name_with_dir,'.zip'])
        print(zip_file_name)
        shutil.make_archive(zip_file_name,'zip',self.__full_path,'.')
        return zip_file_name

    def append_file_suffix(self,suffix=None):
        """添加后缀到目录下的所有文件

        :param suffix:
        :return:
        """
        for item in os.walk(self.__full_path):
            [os.rename(''.join([item[0],'\\',filename]),
                       ''.join([item[0],'\\',PathParse(''.join([item[0],'\\',filename])).file_name_without_extension,suffix,'.',PathParse(''.join([item[0],'\\',filename])).extension]))
             for filename in item[2]]

    @property
    def full_path(self):
        return self.__full_path

    @property
    def path(self):
        return self.__path

    @property
    def parent_path(self):
        return self.__parent_path

    @property
    def relative_path(self):
        return self.__relative_path

    @property
    def relative_parent_path(self):
        return self.__relative_parent_path

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
    print(file_path.find('共享'))
    #file_path.compress()
    file_path.append_file_suffix('@glen#2012%database%mongodb%test')








