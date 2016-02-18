# coding=UTF-8

# --------------------------------------------------------------
# class_filerobot文件
# @class: FileRobot
# @introduction: FileRobot类用来进行文件整理、归档和查询工作
# @dependency: pymongo包
# @author: plutoese
# @date: 2016.01.27
# --------------------------------------------------------------

import os
from datetime import datetime
from libs.file.class_path import Path
from libs.file.class_file import File
from collections import deque
from robots.filerobot.class_osoperator import OSOperator
from robots.filerobot.class_pathtraversal import PathTraversal
from robots.filerobot.class_pathdb import PathDB
from robots.filerobot.class_filedb import FileDB


class FileRobot:
    """ FileRobot类用来进行文件整理、归档和查询工作

    """
    def __init__(self, dirty_path='E:\\room\\forawhile',clean_path='E:\\room\\libs'):
        # 设定类对象的变量
        # 待整理的文件目录
        self.__dirty_path = Path(dirty_path)
        # 整理完成的文件目录
        self.__clean_path = Path(clean_path)
        # 待移动的文件名
        self._to_be_moved = deque()
        # PathTraversal类对象，用来遍历整理完成的文件目录，并把相关信息更新到数据库
        self.__path_traversal = PathTraversal(clean_path)
        # 文件路径数据库
        self.__path_db = PathDB()
        # 文件数据库
        self.__file_db = FileDB()

    def scan_and_copy(self):
        """ 扫描待整理的文件目录，要任务是打包目录或者更新文件名，然后复制到目标目录

        :return: 无返回值
        """
        packed = set()
        special_path = set()

        # 利用os.walk函数遍历文件夹
        for path, _, files in os.walk(self.__dirty_path.absolute_path):
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

        # 把待移动的文件复制到指定的目录
        for file_moved in self._to_be_moved:
            print(file_moved.parser.path_name)
            destination_path = self.__clean_path.find_one(file_moved.parser.dirs)

            if destination_path is None:
                print('Can not find the destination path!')
                raise FileNotFoundError
            OSOperator.copy_to(file_moved.parser.path_name_with_absolute_path,destination_path.absolute_path)

        # 移除原有路径中具有特殊字符路径下文件的特殊字符后缀
        for sp in special_path:
            sp.remove_append_file_suffix()

    def update_database(self):
        """ 更新数据库

        :return: 无返回值
        """
        self.__path_traversal.to_traverse_path()
        self.__path_traversal.close_db()

    def path_tree(self):
        """ 返回来自数据库信息的目录树

        :return: 返回目录树
        :rtype: list
        """
        return self.__file_db.get_files_according_to_path_list(self.__path_db.path_tree())

    def find(self,open_path=r'E:\temp',**condition):
        """ 查询和打开文件窗口

        :param str open_path: 文件打开路径
        :param dict condition: 查询条件
        :return: 返回成功或失败信息
        :rtype: str
        """
        return self.__file_db.find_and_open(self.__clean_path.absolute_path,open_path,**condition)

    @property
    def destination_path(self):
        """ 返回目标路径

        :return: 返回目录路径
        :rtype: Path对象
        """
        return self.__clean_path

if __name__ == '__main__':
    file_robot = FileRobot()
    file_robot.scan_and_copy()
    file_robot.update_database()

    print(file_robot.path_tree())
    file_robot.find(last_modified={'$gt':datetime(2016,2,8)})











