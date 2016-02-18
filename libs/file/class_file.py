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

    def __init__(self, file_name_with_absolute_path):
        # 设定类对象的变量
        # 包含绝对路径的文件名
        self.__file_name_with_absolute_path = None
        # 文件名处理
        self.__file_parser = None
        # 路径
        self.__directory = None

        # 如果输入参数file_name_with_absolute_path不是一个有效的文件名，那么返回错误提示
        if os.path.isfile(file_name_with_absolute_path):
            # 文件全名，即绝对路径加上文件名
            self.__file_name_with_absolute_path = file_name_with_absolute_path
            # 文件名的解析器
            self.__file_parser = PathParser(self.__file_name_with_absolute_path)
            # 文件的绝对路径名
            self.__directory = os.path.split(self.__file_name_with_absolute_path)[0]
        else:
            print('{} is not a valid file!'.format(file_name_with_absolute_path))
            raise FileNotFoundError

    @property
    def file_name(self):
        """ 返回文件全名，即绝对路径加上文件名

        :return: 返回文件全名
        :rtype: str
        """
        return self.__file_name_with_absolute_path

    @property
    def directory(self):
        """ 返回文件的绝对路径名

        :return: 返回文件的绝对路径名
        :rtype: str
        """
        return self.__directory

    @property
    def parser(self):
        """ 返回文件名的解析器

        :return: 返回文件名的解析器
        :rtype: PathParser对象
        """
        return self.__file_parser

    def __len__(self):
        """ 返回文件的大小

        :return: 返回文件的大小
        :rtype: int
        """
        return os.path.getsize(self.__file_name_with_absolute_path)

    def __repr__(self):
        """ 类对象的str表达

        :return: 无返回值
        """
        fmt = ''.join(['file name                  : {0}\n',
                       'directory                  : {1}\n',
                       'size                       : {2}\n'])
        return fmt.format(self.file_name,
                          self.directory,
                          len(self))

if __name__ == '__main__':
    file_path = File(r'E:\room\forawhile\选课手册导出@glen#2012%database%mongodb%test   blank{自科基金{社科基金&econometricsteaching=.zip')
    print(file_path)
    print(type(len(file_path)))
    print(file_path.parser)








