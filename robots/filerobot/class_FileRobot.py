# coding=UTF-8

# --------------------------------------------------------------
# class_FileRobot文件
# @class: FileRobot
# @introduction: FileRobot类用来进行文件整理、归档和查询工作
# @dependency: pymongo包
# @author: plutoese
# @date: 2016.01.27
# --------------------------------------------------------------

import os


class FileRobot:
    """FileRobot类用来进行文件整理、归档和查询工作

    """
    def __init__(self, file_path = 'E:/warehouse'):
        self.__file_path = file_path


    def files_in_path(self, file_path):
        if os.path.isdir(file_path):
            pass
        else:
            print('It is not a file directory!')
            raise FileNotFoundError


if __name__ == '__main__':
    file_robot = FileRobot()








