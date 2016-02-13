# coding=UTF-8

# --------------------------------------------------------------
# class_filedb文件
# @class: FileDB
# @introduction: FileDB类连接filedb数据库
# @dependency: MongoDB，defaultdict，ObjectId及PathDB类，re和os模块
# @author: plutoese
# @date: 2016.02.09
# --------------------------------------------------------------

import re
import os
from collections import defaultdict
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
        # 获得数据库中该文件的路径信息
        path_found = self.__path_db.collection.find_one({'path':path.relative_path})
        if path_found is None:
            print('Path wrong!')
            raise FileNotFoundError
        # 获得文件的信息
        file_found = self.collection.find_one({'full_file_name_without_sc':
                                                   os.path.join(path.relative_path,file.parser.path_name_without_special_characters)})

        # 如果数据库里没有相关文件信息，则插入此文件信息；若有，比较两者是否一致。
        if file_found is not None:
            # 变量fid是数据库中相关文件信息中的_id
            fid = file_found['_id']
            # 目录中文件信息与数据库相关文件信息的差异
            difference = dict(list(self.make_document(file,path,path_found,True).items() - self.make_document_from_db_for_comparision(file_found).items()))
            #更改tags和projects的格式
            if 'tags' in difference:
                difference['tags'] = re.split('\|',difference['tags'])
            if 'projects' in difference:
                difference['projects'] = re.split('\|',difference['projects'])
            if 'last_modified' in difference:
                difference['last_modified'] = file.parser.last_modified
            # 若存在差异，则更新数据库中的信息
            if len(difference) > 0:
                self.collection.find_one_and_update({'_id':fid},
                                                    {'$set':difference})
            return fid
        else:
            # 若数据库中无此文件信息，那么插入此信息
            self.collection.insert_one(self.make_document(file,path,path_found,False))
            return None

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

    def delete_many(self,ids):
         for item in ids:
            self.collection.delete_one({'_id':ObjectId(item)})

    def make_tag_document(self):
        tags = defaultdict(list)
        tag_items = self.collection.find({},{'_id':1,'tags':1})
        for item in tag_items:
            for tag in item['tags']:
                tags[tag].append(item['_id'])
        return tags


    def close(self):
        self.__file_db.close()


if __name__ == '__main__':
    filedb = FileDB()
    filedb.close()
