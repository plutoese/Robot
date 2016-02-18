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
from bson.objectid import ObjectId
from libs.database.class_mongodb import MongoDB


class TagDB:
    """ TagDB类连接tagdb数据库

    """
    def __init__(self):
        # 初始化数据库集合
        self.__tag_db = MongoDB()
        self.__tag_db.connect('FileIndex', 'tagdb')
        self.collection = self.__tag_db.collection

    def update(self,tag):
        """ 更新tagdb数据库

        :param dict tag: tag字典
        :return: 数据库集合tagdb中查询得到的tagid
        :rtype: bson.objectid.ObjectId对象
        """
        tag_found = self.collection.find_one({'tag':tag['tag']})
        if tag_found is not None:
            tagid = tag_found['_id']
            tag_found.pop('_id')
            tag_found['files'] = '|'.join([str(item) for item in tag_found['files']])
            tag['files'] = '|'.join([str(item) for item in tag['files']])
            difference = dict(list(tag.items() - tag_found.items()))
            if len(difference) > 0:
                self.collection.find_one_and_update({'_id':tagid}, {'$set':{'files':tag['files']}})
                                                    #{'$set':{'files':[ObjectId(item) for item in re.split('\|',difference['files'])]}})
            return tagid
        else:
            self.collection.insert_one(tag)
            return None

    def delete_many(self,ids):
        """ 根据id删除数据库中的文档

        :param ids: 数据库中文档的_id列表
        :return: 无返回值
        """
        for item in ids:
            self.collection.delete_one({'_id':ObjectId(item)})

    def close(self):
        """ 关闭数据库连接

        :return: 无返回值
        """
        self.__tag_db.close()


if __name__ == '__main__':
    filedb = TagDB()
    filedb.close()
