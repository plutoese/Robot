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
import re
from datetime import datetime, timedelta
from libs.file.class_path import Path
from libs.file.class_file import File
from collections import deque
from robots.filerobot.class_osoperator import OSOperator
from robots.filerobot.class_pathtraversal import PathTraversal
from robots.filerobot.class_pathdb import PathDB
from robots.filerobot.class_filedb import FileDB

class FileRobot:
    """FileRobot类用来进行文件整理、归档和查询工作

    """
    def __init__(self, dirty_path='E:\\room\\forawhile',clean_path='E:\\room\\libs'):
        self.__dirty_path = Path(dirty_path)
        self.__clean_path = Path(clean_path)
        self._to_be_moved = deque()
        self.__path_traversal = PathTraversal(clean_path)

        self.__path_db = PathDB()
        self.__file_db = FileDB()

    # 扫描dirty_path，主要任务是打包目录或者更新文件名，然后复制到目标目录
    def scan_and_copy(self):
        packed = set()
        special_path = set()
        for path,_,files in os.walk(self.__dirty_path.absolute_path):
            path_obj = Path(path,self.__dirty_path.absolute_path)
            skipped = False

            # 检验是否是打包目录下的子目录，如果是，那么略过
            for packed_item in packed:
                if path_obj.is_child_of(packed_item.absolute_path):
                    skipped = True
                    break
            if skipped:
                continue

            if path_obj.parser.is_packed:
                self._to_be_moved.append(path_obj.compress())
                packed.add(path_obj)
                continue

            # 对于具有特殊字符的目录进行处理
            if path_obj.parser.is_having_special_character:
                files = path_obj.append_file_suffix(path_obj.parser.special_character_part)
                self._to_be_moved.extend([File(file) for file in files])
                packed.add(path_obj)
                special_path.add(path_obj)
                continue

            self._to_be_moved.extend([File(os.path.join(path,file)) for file in files])

        for file_moved in self._to_be_moved:
            print(file_moved.parser.path_name)
            destination_path = self.__clean_path.find_one(file_moved.parser.dirs)

            if destination_path is None:
                print('Can not find the destination path!')
                raise FileNotFoundError
            OSOperator.copy_to(file_moved.parser.path_name_with_absolute_path,destination_path.absolute_path)

        for sp in special_path:
            sp.remove_append_file_suffix()

    # 更新数据库信息
    def update_database(self):
        self.__path_traversal.to_traverse_path()
        self.__path_traversal.close_db()

    # 返回来自数据库信息的目录树
    def path_tree(self):
        return self.__file_db.get_files_according_to_path_list(self.__path_db.path_tree())

    def find(self,open_path=r'E:\temp',**condition):
        return self.__file_db.find_and_open(self.__clean_path.absolute_path,open_path,**condition)

    @property
    def destination_path(self):
        return self.__clean_path

if __name__ == '__main__':
    file_robot = FileRobot()
    file_robot.scan_and_copy()
    file_robot.update_database()

    print(file_robot.path_tree())
    file_robot.find(last_modified={'$gt':datetime(2016,2,8)})











