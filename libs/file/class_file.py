# coding=UTF-8

# --------------------------------------------------------------
# class_file文件
# @class: File
# @introduction: File类用来处理文件
# @dependency: os, os.path包
# @author: plutoese
# @date: 2016.02.09
# --------------------------------------------------------------

import os
from libs.file.class_pathparser import PathParser


class File:
    # 属性
    # 包含绝对路径的文件名
    __file_name_with_absolute_path = None
    # 文件名处理
    __file_parser = None
    # 路径
    __directory = None


    """File类用来处理文件夹

    """
    def __init__(self, file_name_with_absolute_path):
        if os.path.isfile(file_name_with_absolute_path):
            self.__file_name_with_absolute_path = file_name_with_absolute_path
            self.__file_parser = PathParser(self.__file_name_with_absolute_path)
            self.__directory = os.path.split(self.__file_name_with_absolute_path)[0]
        else:
            print('{} is not a valid file!'.format(file_name_with_absolute_path))
            raise FileNotFoundError

    @property
    def file_name(self):
        return self.__file_name_with_absolute_path

    @property
    def directory(self):
        return self.__directory

    @property
    def parser(self):
        return self.__file_parser

    def __len__(self):
        return os.path.getsize(self.file_name)

    def __repr__(self):
        fmt = ''.join(['file name                  : {0}\n',
                       'directory                  : {1}\n',
                       'size                       : {2}\n'])
        return fmt.format(self.file_name,
                          self.directory,
                          len(self))

if __name__ == '__main__':
    file_path = File(r'E:\room\forawhile\选课手册导出@glen#2012%database%mongodb%test   blank{自科基金{社科基金&geeker=.zip')
    print(file_path)
    print(file_path.parser)








