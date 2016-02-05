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


class Path:
    """Path类用来处理文件夹

    """
    def __init__(self, full_path, base_path=None):
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
    file_path = Path('E:\\piles\\teacher','E:\\')
    file_path.walk_and_record()
    print(file_path.full_path)
    print(file_path.path)
    print(file_path.parent_path)
    print('-----------------------')
    print(file_path.relative_path)
    print(file_path.relative_parent_path)
    print(file_path.included)








