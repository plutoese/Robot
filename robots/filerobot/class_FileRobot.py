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
import pickle
from libs.file.class_path import Path
from libs.file.class_pathparse import PathParse
from robots.filerobot.class_osoperator import OSOperator
from libs.database.class_mongodb import MongoDB


class FileRobot:
    """FileRobot类用来进行文件整理、归档和查询工作

    """
    def __init__(self, dirty_path='E:\\room\\forawhile',clean_path='E:\\room\\libs'):
        self.__dirty_path = Path(dirty_path)
        self.__clean_path = Path(clean_path)
        self._to_be_moved = []

        # 初始化数据库集合
        self._path_db, self._file_db, self._tag_db = MongoDB(), MongoDB(), MongoDB()

        self._path_db.connect('FileIndex','pathdb')
        self._file_db.connect('FileIndex','filedb')
        self._tag_db.connect('FileIndex','tagdb')

    def _specil_path_to_file(self):
        special_symbol='[@#$%&{=]'
        for item in os.walk(self.__dirty_path.full_path):
            item_path = Path(item[0])
            if (item_path.is_have_special_symbol()):
                if not item_path.parse.isPacked:
                    suffix = re.split(re.split(special_symbol,item_path.path)[0],item_path.path)[1]
                    item_path.append_file_suffix(suffix)

    def _scan(self):
        packed = []
        for item in os.walk(self.__dirty_path.full_path):
            is_child = False

            print(item[0],Path(item[0]).is_have_special_symbol(),Path(item[0]).parse.isPacked)
            item_path = Path(item[0])
            for packed_item in packed:
                if item_path.is_child_of(packed_item):
                    is_child = True
                    continue
            if is_child:
                continue

            if item_path.parse.isPacked:
                self._to_be_moved.append(item_path.compress())
                packed.append(item[0])
            else:
                self._to_be_moved.extend([''.join([item[0],'\\',file]) for file in item[2]])

    def _file_parse(self):
        moved_files = dict()
        for item in self._to_be_moved:
            parsed_item = PathParse(item)
            move_to_path = parsed_item.dirs
            destination_path = file_robot.destination_path.find(move_to_path)
            print(file_robot.destination_path.find(move_to_path))
            OSOperator.copy_to(item,destination_path)
            moved_files[item] = dict(zip(['file_name','author','last_modified','time','version','tags','project','extension','directory'],
                                         [parsed_item.file_name,parsed_item.author,str(parsed_item.last_modified),
                                          parsed_item.time,parsed_item.version,parsed_item.tags,parsed_item.project,
                                          parsed_item.extension,destination_path]))

    @property
    def destination_path(self):
        return self.__clean_path

if __name__ == '__main__':
    file_robot = FileRobot()
    #file_robot._specil_path_to_file()
    #file_robot._scan()

    FILE = open('d:\\down\\datafile.pkl', 'rb')
    #pickle.dump(file_robot._to_be_moved,FILE)
    #FILE.close()

    to_be_moved = pickle.load(FILE)
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    moved_files = dict()
    for item in to_be_moved:
        parsed_item = PathParse(item)
        move_to_path = parsed_item.dirs
        destination_path = file_robot.destination_path.find(move_to_path)
        print(file_robot.destination_path.find(move_to_path))
        OSOperator.copy_to(item,destination_path)
        moved_files[item] = dict(zip(['file_name','author','last_modified','time','version','tags','project','extension','directory'],
                                     [parsed_item.file_name,parsed_item.author,str(parsed_item.last_modified),
                                      parsed_item.time,parsed_item.version,parsed_item.tags,parsed_item.project,
                                      parsed_item.extension,destination_path]))
        #file_robot._file_db.collection.insert_one({moved_files[item]})
        print(moved_files[item])


    for key in moved_files:
        print(key,'-->',moved_files[key])









