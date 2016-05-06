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
from collections import defaultdict, OrderedDict
from bson.objectid import ObjectId
from libs.database.class_mongodb import MongoDB
from robots.filerobot.class_pathdb import PathDB
from datetime import datetime
from robots.filerobot.class_osoperator import OSOperator


class FileDB:
    """ FileDB类连接filedb数据库

    """
    def __init__(self):
        # 初始化数据库集合
        self.__file_db = MongoDB()
        self.__file_db.connect('FileIndex', 'filedb')
        self.collection = self.__file_db.collection
        # pathdb数据集合
        self.__path_db = PathDB()

    def update(self,file,path):
        """ 根据file，更新文件库信息

        :param file: 文件对象
        :param path: 路径对象
        :return: 返回当前文件在数据库中的id，如果数据库中无当前文件信息，返回None
        :rtype: bson.objectid.ObjectId对象
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
            difference = dict(list(self.make_document(file,path,path_found,True).items() - self.make_document_from_db(file_found).items()))
            # 更改tags和projects的格式
            if 'tags' in difference:
                difference['tags'] = re.split('\|',difference['tags'])
            if 'projects' in difference:
                difference['projects'] = re.split('\|',difference['projects'])
            if 'last_modified' in difference:
                difference['last_modified'] = file.parser.last_modified
            if 'time' in difference:
                difference['time'] = file.parser.time
            # 若存在差异，则更新数据库中的信息
            if len(difference) > 0:
                self.collection.insert_one(self.make_document(file,path,path_found,False))
                return None
            else:
                #self.collection.find_one_and_update({'_id':fid},{'$set':difference})
                return fid
        else:
            # 若数据库中无此文件信息，那么插入此信息
            self.collection.insert_one(self.make_document(file,path,path_found,False))
            return None

    @classmethod
    def make_document(cls,file,path,path_found,for_comparison=False):
        """ 根据file，path以及数据库中查询得到的path_found，创建符合数据库filedb集合标准格式的文档

        :param File file: 文件对象
        :param Path path: 路径对象
        :param dict path_found: 数据库中查询得到的路径文档
        :param bool for_comparison: 是否是用来进行比较
        :return: 数据文档
        :rtype: dict
        """
        if for_comparison:
            document = {'full_file_name': os.path.join(path.relative_path,file.parser.path_name),
                        'full_file_name_without_sc': os.path.join(path.relative_path,file.parser.path_name_without_special_characters),
                        'special_characters': file.parser.special_character_part,
                        'file_name': file.parser.path_name,
                        'directory': path_found['_id'],
                        'extension': file.parser.extension,
                        'last_modified': file.parser.last_modified.ctime(),
                        'size': len(file),
                        'author': file.parser.author,
                        'version': file.parser.version}
            if file.parser.time is not None:
                document['time'] = file.parser.time.ctime()
            else:
                document['time'] = None
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

    @classmethod
    def make_document_from_db(cls,file):
        """ 根据数据库中的文件文档对象创建新文档，进行比较

        :param dict file: 文件对象
        :return: 文档
        :rtype: dict
        """
        record = file
        record.pop('_id')
        record['last_modified'] = record['last_modified'].ctime()

        if record['time'] is not None:
            record['time'] = record['time'].ctime()
        else:
            record['time'] = None

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
        """ 根据id删除数据库中的文档

        :param ids: 数据库中文档的_id列表
        :return: 无返回值
        """
        for item in ids:
            self.collection.delete_one({'_id':ObjectId(item)})

    def make_tag_document(self):
        """ 根据filedb数据库中的信息，生成tagdb中所需要的标准格式文档

        :return: 标签文档
        :rtype: defaultdict对象
        """
        tags = defaultdict(list)
        tag_items = self.collection.find({},{'_id':1,'tags':1})
        for item in tag_items:
            for tag in item['tags']:
                tags[tag].append(item['_id'])
        return tags

    def get_files_according_to_path_list(self,path_list):
        """ 根据目录列表，补充文件信息

        :param list path_list: 目录列表
        :return: 完整的目录文件字典
        :rtype: OrderedDict对象
        """
        result = OrderedDict()
        for path in path_list:
            path_found = self.__path_db.collection.find_one({'path':path})
            files_found = self.collection.find({'directory':path_found['_id']})
            result[path] = [file['file_name'] for file in files_found]
        return result

    def find_and_open(self,base_path,temp_path,**condition):
        """ 根据condition条件查询filedb数据库，复制查询得到的文件到temp_path，并且打开temp_path文件窗口

        :param str base_path:
        :param str temp_path:
        :param dict condition:
        :return: 返回成功或失败信息
        :rtype: str
        """
        result = list(self.collection.find(condition))
        if len(result) < 1:
            return "None is found!"
        else:
            for item in result:
                source_file = os.path.join(base_path,item['full_file_name'])
                destination_file = os.path.join(temp_path,item['file_name'])
                OSOperator.copy_to(source_file,destination_file)
            os.startfile(temp_path)
            return "successfully!"

    def close(self):
        """ 关闭数据库连接

        :return: 无返回值
        """
        self.__file_db.close()


if __name__ == '__main__':
    filedb = FileDB()
    path_list = ['teacher', 'teacher\\econometricsteaching', 'teacher\\tutor', 'geeker', 'geeker\\python', 'geeker\\python\\books', 'geeker\\R', 'geeker\\R\\Rstudio', 'geeker\\R\\Rstudio\\book']
    filedb.get_files_according_to_path_list(path_list)

    base_path = 'E:\\room\\libs'
    temp_path = 'E:\\temp'
    filedb.find_and_open(base_path,temp_path,last_modified={'$gt':datetime(2016,2,8)})
    filedb.close()
