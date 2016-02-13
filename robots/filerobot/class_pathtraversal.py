# coding=UTF-8

# --------------------------------------------------------------
# class_pathtraversal文件
# @class: PathTraversal
# @introduction: PathTraversal类遍历文件夹更新数据库
# @dependency: File, Path类
# @author: plutoese
# @date: 2016.02.08
# --------------------------------------------------------------

import os
from libs.file.class_path import Path
from libs.file.class_file import File
from robots.filerobot.class_pathdb import PathDB
from robots.filerobot.class_filedb import FileDB
from robots.filerobot.class_tagdb import TagDB


class PathTraversal:
    # 属性
    # 绝对路径
    __path = None

    """PathTraversal类遍历文件夹更新数据库

    """
    def __init__(self, absolute_path):
        # 设置文件库路径名称
        self.__path = Path(absolute_path)

        # 初始化数据库集合
        self.path_db = PathDB()
        self.file_db = FileDB()
        self.tag_db = TagDB()

        # path，file和tag数据库中所有文档的_id集合
        self.path_set = set(item['_id'] for item in self.path_db.collection.find({},{'_id':1}))
        self.file_set = set(item['_id'] for item in self.file_db.collection.find({},{'_id':1}))
        self.tag_set = set(item['_id'] for item in self.tag_db.collection.find({},{'_id':1}))

    def to_update_path_and_file_db(self):
        pass

    def to_traverse_path(self):
        """ 遍历目录，更新数据库

        :return: 无返回值
        """
        # path是绝对路径，files是文件列表
        # self.path.included返回的是os.walk函数的结果，即列表，列表的三个元素分别是绝对路径，子目录名称以及文件
        for path,_,files in self.path.included:
            # Path类对象，输入参数为绝对路径
            path_obj = Path(path,self.path.absolute_path)
            # pathid是相对路径的数据库_id
            pathid = self.path_db.update(path_obj)
            # 如果path存在于数据库中，则删除集合path_set中对应的path，这一步是为了删除数据库中无用的路径
            if pathid is not None:
                self.path_set.remove(pathid)

            # 插入文件信息
            if len(files) > 0:
                for file in files:
                    # 更新文件信息
                    # 调用FileDB类对象的update方法，输入参数为文件的File对象及其所在路径的Path对象
                    fileid = self.file_db.update(File(os.path.join(path,file)),path_obj)
                    if fileid is not None:
                        self.file_set.remove(fileid)

        # 删除数据库中无用的路径信息
        self.path_db.delete_many(self.path_set)
        # 删除数据库中无用的文件信息
        self.file_db.delete_many(self.file_set)
        # 设置路径的子目录集合
        self.path_db.traverse_and_update()

        tags = self.file_db.make_tag_document()
        for tag in tags:
            tag_dict = {'tag':tag,'files':tags[tag]}
            tagid = self.tag_db.update(tag_dict)
            if tagid is not None:
                self.tag_set.remove(tagid)

        self.tag_db.delete_many(self.tag_set)

    @property
    def path(self):
        return self.__path

    def close_db(self):
        self.path_db.close()
        self.file_db.close()
        self.tag_db.close()


if __name__ == '__main__':
    file_path = PathTraversal(r'E:\room\libs')
    file_path.to_traverse_path()
    file_path.close_db()
