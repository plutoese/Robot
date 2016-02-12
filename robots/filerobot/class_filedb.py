# coding=UTF-8

# --------------------------------------------------------------
# class_filedb文件
# @class: FileDB
# @introduction: FileDB类连接filedb数据库
# @dependency: MongoDB类
# @author: plutoese
# @date: 2016.02.09
# --------------------------------------------------------------

import re
import os
from bson.objectid import ObjectId
from libs.database.class_mongodb import MongoDB
from robots.filerobot.class_pathdb import PathDB


class FileDB:
    """FileDB类连接filedb数据库

    """
    def __init__(self):
        # 初始化数据库集合
        self.__file_db = MongoDB()
        self.__file_db.connect('FileIndex', 'filedb')
        self.collection = self.__file_db.collection

        self.__path_db = PathDB()

    def update(self,file,path):
        """ 更新文件库信息

        :param file:
        :param path:
        :return:
        """
        # 获得文件的路径信息
        path_found = self.__path_db.collection.find_one({'path':path.relative_path})
        if path_found is None:
            print('Path wrong!')
            raise FileNotFoundError

        file_found = self.collection.find_one({'full_file_name_without_sc':
                                                   os.path.join(path.relative_path,file.parser.path_name_without_special_characters)})

        if file_found is not None:
            fid = file_found['_id']
            print('what the hell>>>>>>>>>>>>>>>>>>>>>>>>>')
            different = dict(list(self.make_document(file,path,path_found,True).items() - self.make_document_from_db_for_comparision(file_found).items()))
            if 'tags' in different:
                different['tags'] = re.split('\|',different['tags'])
            if 'projects' in different:
                different['projects'] = re.split('\|',different['projects'])
            print(different)
            if len(different) > 0:
                print(file_found)
                self.collection.find_one_and_update({'_id':fid},
                                                    {'$set':different})
        else:
            self.collection.insert_one(self.make_document(file,path,path_found,False))

    def make_document(self,file,path,path_found,for_comparision=False):
        if for_comparision:
            document = {'full_file_name': os.path.join(path.relative_path,file.parser.path_name),
                        'full_file_name_without_sc': os.path.join(path.relative_path,file.parser.path_name_without_special_characters),
                        'special_characters': file.parser.special_character_part,
                        'file_name': file.parser.path_name,
                        'directory': path_found['_id'],
                        'extension': file.parser.extension,
                        'last_modified': file.parser.last_modified.ctime(),
                        'size': len(file),
                        'author': file.parser.author,
                        'time': file.parser.time,
                        'version': file.parser.version}
            if file.parser.tags is not None:
                document['tags'] = '|'.join(file.parser.tags)
            else:
                document['tags'] = None

            if file.parser.projects is not None:
                document['projects'] = '|'.join(file.parser.projects)
            else:
                document['projects'] = None
        else:
            document = {'full_file_name': os.path.join(path.relative_path,file.parser.path_name),
                        'full_file_name_without_sc': os.path.join(path.relative_path,file.parser.path_name_without_special_characters),
                        'special_characters': file.parser.special_character_part,
                        'file_name': file.parser.path_name,
                        'directory': path_found['_id'],
                        'extension': file.parser.extension,
                        'last_modified': file.parser.last_modified,
                        'size': len(file),
                        'author': file.parser.author,
                        'time': file.parser.time,
                        'version': file.parser.version,
                        'tags': file.parser.tags,
                        'projects': file.parser.projects}

        return document

    def make_document_from_db_for_comparision(self,file):
        record = file
        record.pop('_id')
        record['last_modified'] = record['last_modified'].ctime()
        if record['tags'] is not None:
            record['tags'] = '|'.join(record['tags'])
        else:
            record['tags'] = None

        if record['projects'] is not None:
            record['projects'] = '|'.join(record['projects'])
        else:
            record['projects'] = None
        return record

    def close(self):
        self.__file_db.close()


if __name__ == '__main__':
    filedb = FileDB()
    filedb.close()
