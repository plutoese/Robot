# coding=UTF-8

# --------------------------------------------------------------
# class_pathdb文件
# @class: PathDB
# @introduction: PathDB类连接pathdb数据库
# @dependency: MongoDB类
# @author: plutoese
# @date: 2016.02.09
# --------------------------------------------------------------

import re
from bson.objectid import ObjectId
from libs.database.class_mongodb import MongoDB


class PathDB:
    """PathDB类连接pathdb数据库

    """
    def __init__(self):
        # 初始化数据库集合
        self.__path_db = MongoDB()
        self.__path_db.connect('FileIndex', 'pathdb')
        self.collection = self.__path_db.collection

    def update(self,path):
        document_in_db = self.collection.find_one({'path':path.relative_path})
        if document_in_db is None:
            # 匹配path_parent_id
            if re.match('^\.$',path.relative_path) is not None:
                self.collection.insert_one({'path':path.relative_path,
                                            'path_name':path.relative_path,
                                            'parent_path_id':None,
                                            'last_modified':path.parser.last_modified,
                                            'children_id':[]})
            else:
                parent_id = self.collection.find_one({'path':path.relatvie_parent_path})['_id']
                self.collection.insert_one({'path':path.relative_path,
                                            'path_name': path.current_path,
                                            'parent_path_id':parent_id,
                                            'last_modified':path.parser.last_modified,
                                            'children_id':[]})
            return None
        else:
            if (path.parser.last_modified - document_in_db['last_modified']).total_seconds() > 0.01:
                self.collection.find_one_and_update({'_id':document_in_db['_id']},
                                                    {'$set':{'last_modified':path.parser.last_modified}})
            return document_in_db['_id']

    def traverse_and_update(self):
        for record in self.collection.find({}):
            if record.get('parent_path_id') is not None:
                self.collection.update_one({'_id':record.get('parent_path_id')},
                                           {'$addToSet':{'children_id':record.get('_id')}},
                                           upsert =True)

    def delete_many(self,ids):
         for item in ids:
            self.collection.delete_one({'_id':ObjectId(item)})

    def close(self):
        self.__path_db.close()


if __name__ == '__main__':
    pathdb = PathDB()
    pathdb.close()
