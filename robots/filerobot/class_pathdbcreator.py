# coding=UTF-8

# --------------------------------------------------------------
# class_PathDataBaseCreator文件
# @class: PathDataBaseCreator
# @introduction: PathDataBaseCreator类用来通过文件夹创建数据库
# @dependency: File, Path类
# @author: plutoese
# @date: 2016.01.28
# --------------------------------------------------------------

import re
import os
from libs.file.class_file import File
from libs.file.class_path import Path
from libs.database.class_mongodb import MongoDB

class PathDataBaseCreator:
    """PathDataBaseCreator类用来通过文件夹创建数据库

    """
    def __init__(self, path):
        self.__path_name = path
        self.__path = Path(self.__path_name)

        # 初始化数据库集合
        self.__path_db, self.__file_db, self.__tag_db = MongoDB(), MongoDB(), MongoDB()

        self.__path_db.connect('FileIndex','pathdb')
        self.__file_db.connect('FileIndex','filedb')
        self.__tag_db.connect('FileIndex','tagdb')

        for db in [self.__path_db, self.__file_db, self.__tag_db]:
            if db.collection.count() > 0:
                db.collection.delete_many({})

    def to_create_path_and_file_db(self):

        tags = dict()

        for dirpath,dirname,filenames in self.__path.included:
            print(dirpath,' --> ',dirname,' ==> ',filenames)
            print(Path(dirpath,self.__path_name).relative_path,Path(dirpath,self.__path_name).relative_parent_path)
            print('********************************')

            # 匹配path_parent_id
            path_parent = Path(dirpath,self.__path_name).relative_parent_path
            if re.match('^\.\.$',path_parent) is not None:
                self.__path_db.collection.insert_one({'path':Path(dirpath,self.__path_name).relative_path,
                                                      'path_name': Path(dirpath,self.__path_name).path,
                                                      'parent_path_id':None,
                                                      'children_id':[]})
            else:
                path_parent_id = self.__path_db.collection.find_one({'path':path_parent})['_id']
                self.__path_db.collection.insert_one({'path':Path(dirpath,self.__path_name).relative_path,
                                                      'path_name': Path(dirpath,self.__path_name).path,
                                                      'parent_path_id':path_parent_id,
                                                      'children_id':[]})

            # 插入文件信息
            if len(filenames) > 0:
                for file in filenames:
                    mfile = File(os.path.join(dirpath,file))
                    file_tags = mfile.tags
                    print(mfile.file_name_with_dir)
                    self.__file_db.collection.insert_one({
                        'full_file_name': mfile.file_name_with_dir,
                        'file_name': mfile.file_name,
                        'directory': self.__path_db.collection.find_one({'path':Path(dirpath,self.__path_name).relative_path})['_id'],
                        'extension': mfile.extension,
                        'last_modified': mfile.last_modified,
                        'size': len(mfile),
                        'author': mfile.author,
                        'time': mfile.time,
                        'version': mfile.version,
                        'tags': file_tags
                    })
                    if file_tags is not None:
                        for tag in file_tags:
                            print(mfile.file_name_with_dir)
                            tags.setdefault(tag,[]).append(self.__file_db.collection.find_one({'full_file_name':mfile.file_name_with_dir})['_id'])

        print(tags)
        for key in tags:
            self.__tag_db.collection.insert_one({'tag':key,'files':tags[key]})

        children_ids = dict()
        for record in self.__path_db.collection.find({}):
            print(record.get('_id'))
            if record.get('parent_path_id') is not None:
                self.__path_db.collection.update_one({'_id':record.get('parent_path_id')},
                                                    {'$addToSet':{'children_id':record.get('_id')}},
                                                     upsert =True)

    def close_db(self):
        self.__path_db.close()
        self.__file_db.close()
        self.__tag_db.close()

if __name__ == '__main__':
    file_path = PathDataBaseCreator('E:\\piles')
    file_path.to_create_path_and_file_db()
    file_path.close_db()




