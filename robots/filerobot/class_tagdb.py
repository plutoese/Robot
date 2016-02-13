# coding=UTF-8

# --------------------------------------------------------------
# class_tagdb文件
# @class: TagDB
# @introduction: TagDB类连接tagdb数据库
# @dependency: MongoDB类
# @author: plutoese
# @date: 2016.02.09
# --------------------------------------------------------------

import re
import os
from collections import defaultdict
from bson.objectid import ObjectId
from libs.database.class_mongodb import MongoDB
from robots.filerobot.class_pathdb import PathDB


class TagDB:
    """FileDB类连接filedb数据库

    """
    def __init__(self):
        # 初始化数据库集合
        self.__tag_db = MongoDB()
        self.__tag_db.connect('FileIndex', 'tagdb')
        self.collection = self.__tag_db.collection

    def update(self,tag):
        tag_found = self.collection.find_one({'tag':tag['tag']})
        if tag_found is not None:
            tagid = tag_found['_id']
            tag_found.pop('_id')
            tag_found['files'] = '|'.join([str(item) for item in tag_found['files']])
            tag['files'] = '|'.join([str(item) for item in tag['files']])
            difference = dict(list(tag.items() - tag_found.items()))
            if len(difference) > 0:
                self.collection.find_one_and_update({'_id':tagid},
                                                    {'$set':{'files':[ObjectId(item) for item in re.split('\|',difference['files'])]}})
            return tagid
        else:
            self.collection.insert_one(tag)
            return None

    def delete_many(self,ids):
         for item in ids:
            self.collection.delete_one({'_id':ObjectId(item)})

    def close(self):
        self.__tag_db.close()


if __name__ == '__main__':
    filedb = TagDB()
    filedb.close()
