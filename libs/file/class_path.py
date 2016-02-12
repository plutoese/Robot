# coding=UTF-8

# --------------------------------------------------------------
# class_path文件
# @class: Path
# @introduction: Path类用来处理文件夹
# @dependency: os, os.path包
# @author: plutoese
# @date: 2016.01.28
# --------------------------------------------------------------

import os
import re
from libs.file.class_pathparser import PathParser
from libs.file.class_file import File
import shutil


class Path:
    # 属性
    # 绝对路径
    __absolute_path = None
    # 基础路径，用来演算相对路径
    __base_path = None
    # 父路径
    __absolute_parent_path = None
    # 当前路径
    __current_path = None
    # 相对路径
    __relative_path = None
    # 相对父路径
    __relatvie_parent_path = None
    # 目录名处理
    __path_parser = None

    """Path类用来处理文件夹

    """

    def __init__(self, absolute_path, base_path=None):
        if os.path.isdir(absolute_path):
            self.__absolute_path = absolute_path
            self.__path_parser = PathParser(self.__absolute_path)
            # self.__absolute_parent_path是父目录
            # self.__current_path是当前目录
            self.__absolute_parent_path, self.__current_path = os.path.split(self.__absolute_path)
        else:
            print('{} is not a directory!'.format(self.__absolute_path))
            raise FileNotFoundError

        if base_path is not None:
            if os.path.isdir(absolute_path):
                self.__base_path = base_path
                self.__relative_path = os.path.relpath(self.__absolute_path, self.__base_path)
                self.__relatvie_parent_path = os.path.relpath(self.__absolute_parent_path, self.__base_path)
            else:
                print('{} is not a directory!'.format(self.base_path))
                raise FileNotFoundError

    # 通过路径名寻找路径
    def find_all(self, keyword, perfect=True):
        """通过关键词寻找路径

        :param str,list keyword: 路径名称关键字
        :param bool perfect: 是否完美匹配
        :return: 路径
        :rtype: Path类对象
        """
        if isinstance(keyword, str):
            return self.find_by_string(keyword, perfect)
        elif isinstance(keyword, (tuple, list)):
            return self.find_by_string(keyword[0], perfect)
        else:
            raise TypeError

    # 通过路径名寻找路径
    def find_one(self, keyword, perfect=True):
        """通过关键词寻找路径

        :param str,list keyword: 路径名称关键字
        :param bool perfect: 是否完美匹配
        :return: 路径
        :rtype: Path类对象
        """
        if isinstance(keyword, str):
            return self.find_by_string(keyword, perfect, False)
        elif isinstance(keyword, (tuple, list)):
            return self.find_by_list(keyword, perfect)
        else:
            raise TypeError

    def find_by_string(self, piece, perfect, all=True):
        """通过字符串寻找路径

        :param piece:
        :param perfect:
        :return:
        """
        result = []
        for item in os.walk(self.__absolute_path):
            if perfect:
                if os.path.split(item[0])[1] == piece:
                    result.append(Path(item[0], self.base_path))
            else:
                if os.path.split(item[0])[1].find(piece) > -1:
                    result.append(Path(item[0], self.base_path))

        if len(result) < 1:
            return None
        else:
            if all:
                return result
            else:
                return result[0]

    def find_by_list(self, pieces, perfect):
        """通过列表寻找路径

        :param pieces:
        :param perfect:
        :return:
        """
        base_path = self.__absolute_path
        for piece in pieces:
            for item in os.walk(base_path):
                if perfect:
                    if os.path.split(item[0])[1] == piece:
                        base_path = item[0]
                        break
                else:
                    if os.path.split(item[0])[1].find(piece) > -1:
                        base_path = item[0]
                        break

        if base_path == self.__absolute_path:
            return None
        else:
            return Path(base_path,self.base_path)

    def compress(self):
        """压缩目录为zip文件，并且返回zip文件的完整目录

        :return:
        """
        shutil.make_archive(self.absolute_path,'zip',self.absolute_path,'.')
        return File(''.join([self.absolute_path,'.zip']))

    def append_file_suffix(self,suffix=None):
        """添加后缀到目录下的所有文件

        :param suffix:
        :return:
        """
        for item in os.walk(self.__absolute_path):
            [os.rename(''.join([item[0],'\\',filename]),
                       ''.join([item[0],'\\',PathParser(''.join([item[0],'\\',filename])).path_name_without_extension,suffix,'.',PathParser(''.join([item[0],'\\',filename])).extension]))
             for filename in item[2]]

    def is_child_of(self,new_path):
        """测试是否为某目录的子目录

        :param new_path: 某目录
        :return:
        """
        if not os.path.isdir(new_path):
            print('{} is not a valid path.'.format(new_path))
            raise TypeError
        else:
            normal_new_path = os.path.normpath(new_path)
            print(normal_new_path,self.absolute_parent_path)
            if normal_new_path == self.absolute_parent_path:
                return True
            else:
                return False

    @property
    def absolute_path(self):
        return os.path.normpath(self.__absolute_path)

    @property
    def base_path(self):
        if self.__base_path is not None:
            return os.path.normpath(self.__base_path)
        return None

    @property
    def absolute_parent_path(self):
        if self.__absolute_parent_path is not None:
            return os.path.normpath(self.__absolute_parent_path)
        return None

    @property
    def current_path(self):
        if self.__current_path is not None:
            return os.path.normpath(self.__current_path)
        return None

    @property
    def relative_path(self):
        if self.__relative_path is not None:
            return os.path.normpath(self.__relative_path)
        return None

    @property
    def relatvie_parent_path(self):
        if self.__relatvie_parent_path is not None:
            return os.path.normpath(self.__relatvie_parent_path)
        return None

    @property
    def parser(self):
        return self.__path_parser

    @property
    def included(self):
        return os.walk(self.absolute_path)

    def __repr__(self):
        fmt = ''.join(['absolute path                       : {0}\n',
                       'base path                           : {1}\n',
                       'absolute parent path                : {2}\n',
                       'current path                        : {3}\n',
                       'relative path                       : {4}\n',
                       'relatvie parent path                : {5}\n'])
        return fmt.format(self.absolute_path,
                          self.base_path,
                          self.absolute_parent_path,
                          self.current_path,
                          self.relative_path,
                          self.relatvie_parent_path
                          )


if __name__ == '__main__':
    file_path = Path(r'E:\room\forawhile\personalnote@glen#2012%note&researchproject', r'E:\room')
    print(file_path.find_one(['guess','good'], False))
    print(file_path.compress())
    print(file_path.is_child_of(r'E:\room\forawhile'))
