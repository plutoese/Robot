# coding=UTF-8

# --------------------------------------------------------------
# class_pathdb文件
# @class: PathDB
# @introduction: PathDB类连接pathdb数据库
# @dependency: MongoDB类，ObjectId类及re模块
# @author: plutoese
# @date: 2016.02.09
# --------------------------------------------------------------

import re
from bson.objectid import ObjectId
from libs.database.class_mongodb import MongoDB


class PathDB:
    """ PathDB类连接pathdb数据库

    """
    def __init__(self):
        # 初始化数据库集合
        self.__path_db = MongoDB()
        self.__path_db.connect('FileIndex', 'pathdb')
        self.collection = self.__path_db.collection

    def update(self,path):
        """ 更新路径

        :param Path path: Path类对象，提供路径信息
        :return: 数据库匹配得到的路径文档的_id，若数据库中不存在此路径，则返回None
        :rtype: ObjectId类对象或者None
        """
        # 根据相对路径寻找数据库中匹配的文档
        document_in_db = self.collection.find_one({'path':path.relative_path})
        # 若没有找到匹配的文档，则插入当前路径信息文档
        if document_in_db is None:
            self.collection.insert_one(self.make_document(path,False))
            return None
        else:
            # 更新数据库路径文档
            did = document_in_db['_id']
            document_in_db.pop('_id')
            document_in_db.pop('children_id')
            document_in_db['last_modified'] = document_in_db['last_modified'].ctime()

            difference = dict(list(self.make_document(path,True).items() - document_in_db.items()))
            if 'last_modified' in difference:
                difference['last_modified'] = path.parser.last_modified
            if len(difference) > 0:
                self.collection.find_one_and_update({'_id':did},{'$set':difference})

            return did

    def traverse_and_update(self):
        """ 遍历更新路径文档的子目录信息，即childre_id。
        这里分两个步骤，其一是遍历数据库，通过原文档的父路径id，查询父路径文档，并把源文档的id添加到父路径文档的children_id中；
        其二是遍历数据库，通过源文档的子路径id列表，查询子路径文档，并验证该子路径是否存在

        :return: 无返回值
        """
        # 遍历数据库
        for record in self.collection.find({}):
            # 获得单个记录的父路径id
            record_parent_path_id = record['parent_path_id']
            if record_parent_path_id is not None:
                # 查询父路径id指向的记录，则指向的记录是当前记录的父路径记录，那么该父路径的子路径集中必须有当前记录信息
                children_id = set(self.collection.find_one({'_id':record_parent_path_id})['children_id'])
                if record['_id'] not in children_id:
                    self.collection.update_one({'_id':record_parent_path_id},
                                               {'$addToSet':{'children_id':record.get('_id')}},upsert =True)

        # 遍历数据库
        for record in self.collection.find({}):
            # 如果存在子目录集合，那么查询每个子目录是否存在
            if len(record['children_id']) > 0:
                for pid in record['children_id']:
                    path_found = self.collection.find_one({'_id':pid})
                    if path_found is None:
                        self.collection.update_one({'_id':record['_id']},
                                                   {'$pull':{'children_id':pid}})
                        continue
                    if path_found['parent_path_id'] != record['_id']:
                        self.collection.update_one({'_id':record['_id']},
                                                   {'$pull':{'children_id':pid}})

    def make_document(self,path,for_comparison=False):
        """ 根据path创建标准格式的数据库pathdb集合中的文档

        :param path:
        :param for_comparision:
        :return:
        """
        # 数据库中文档形式如下：
        # {
        #    path: 相对路径
        #    path_name: 当前路径名称
        #    parent_path_id: 相对父路径
        #    last_modified: 最近修改时间
        #    children_id: 子目录列表
        # }
        if for_comparison:
            # 根目录是.，如果是根目录，需要设置parent_path_id为None
            if re.match('^\.$',path.relative_path) is not None:
                document = {'path':path.relative_path,
                            'path_name':path.relative_path,
                            'parent_path_id':None,
                            'last_modified':path.parser.last_modified.ctime()}
            else:
                parent_id = self.collection.find_one({'path':path.relatvie_parent_path})['_id']
                document = {'path':path.relative_path,
                            'path_name': path.current_path,
                            'parent_path_id':parent_id,
                            'last_modified':path.parser.last_modified.ctime()}
        else:
            # 根目录是.，如果是根目录，需要设置parent_path_id为None
            if re.match('^\.$',path.relative_path) is not None:
                document = {'path':path.relative_path,
                            'path_name':path.relative_path,
                            'parent_path_id':None,
                            'last_modified':path.parser.last_modified,
                            'children_id':[]}
            else:
                parent_id = self.collection.find_one({'path':path.relatvie_parent_path})['_id']
                document = {'path':path.relative_path,
                            'path_name': path.current_path,
                            'parent_path_id':parent_id,
                            'last_modified':path.parser.last_modified,
                            'children_id':[]}

        return document

    def _raw_path_tree(self,root='.'):
        """ 辅助函数，根据数据库中的信息，返回目录树

        :param str root: 起始路径
        :return: 路径树
        :rtype: list
        """
        result = []
        # 查询起始路径
        root_path = self.collection.find_one({'path':root})
        # 查询子路径集合
        child_path = list(self.collection.find({'parent_path_id':root_path['_id']}))
        # 如果没有子路径，则返回当前路径的集合
        if len(child_path) < 1:
            return [root_path['path']]
        # 否则，添加子路径及以子路径为起始路径的下属路径
        else:
            for item in child_path:
                result.append(item['path'])
                result.extend(self._raw_path_tree(item['path']))
            return result

    def path_tree(self,root='.'):
        """ 根据数据库中的信息，返回目录树

        :param str root: 起始路径
        :return: 路径树
        :rtype: list
        """
        # 这里result_set的用途是排除重合的路径
        result_set = set()
        raw_result = self._raw_path_tree(root)
        result = []
        for item in raw_result:
            if item not in result_set:
                result.append(item)
                result_set.add(item)

        return result

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
        self.__path_db.close()


if __name__ == '__main__':
    pathdb = PathDB()
    print(pathdb._raw_path_tree())
    print(pathdb.path_tree())
    pathdb.close()
