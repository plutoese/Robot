# coding=UTF-8

# --------------------------------------------------------------
# class_PathDBupdater文件
# @class: PathDBupdater
# @introduction: PathDBupdater类用来通过文件夹更新数据库
# @dependency: File, Path类
# @author: plutoese
# @date: 2016.02.08
# --------------------------------------------------------------

import re
import os
from libs.file.class_pathparse import PathParse
from libs.file.class_path import Path
from libs.database.class_mongodb import MongoDB


class PathDBupdater:
    """PathDBupdater类用来通过文件夹更新数据库

    """

    def __init__(self, path):
        # 设置文件库路径名称
        self.__path_name = path
        self.__path = Path(self.__path_name)

        # 初始化数据库集合
        self.__path_db, self.__file_db, self.__tag_db = MongoDB(), MongoDB(), MongoDB()

        self.__path_db.connect('FileIndex', 'pathdb')
        self.__file_db.connect('FileIndex', 'filedb')
        self.__tag_db.connect('FileIndex', 'tagdb')

    def to_update_path_and_file_db(self):

        path_dict = {item['path']:item['last_modified'] for item in self.__path_db.collection.find({},{'path':1,'_id':0,'last_modified':1})}
        file_dict = {item['full_file_name']:item['last_modified'] for item in self.__file_db.collection.find({},{'full_file_name':1,'_id':0,'last_modified':1})}

        tags = dict()

        for dirpath, dirname, filenames in self.__path.included:
            #print(dirpath, ' --> ', dirname, ' ==> ', filenames)
            #print(Path(dirpath, self.__path_name).relative_path, Path(dirpath, self.__path_name).relative_parent_path)
            #print('********************************')

            dpath = Path(dirpath,self.__path_name)
            '''
            print('nnnnnnnnnnnnnnn',dpath.parse.last_modified,self.path_dict[dpath.relative_path])
            print('minus:',dpath.parse.last_modified - self.path_dict[dpath.relative_path])
            print('=====:',(dpath.parse.last_modified - self.path_dict[dpath.relative_path]).total_seconds()>0.01)'''

            path_record = self.__path_db.collection.find_one({'path':dpath.relative_path})

            if path_record is None:
                # 匹配path_parent_id
                path_parent = Path(dirpath,self.__path_name).relative_parent_path
                if re.match('^\.\.$',path_parent) is not None:
                    self.__path_db.collection.insert_one({'path':dpath.relative_path,
                                                          'path_name': dpath.path,
                                                          'parent_path_id':None,
                                                          'last_modified':dpath.parse.last_modified,
                                                          'children_id':[]})
                else:
                    path_parent_id = self.__path_db.collection.find_one({'path':path_parent})['_id']
                    self.__path_db.collection.insert_one({'path':dpath.relative_path,
                                                          'path_name': dpath.path,
                                                          'parent_path_id':path_parent_id,
                                                          'last_modified':dpath.parse.last_modified,
                                                          'children_id':[]})
            else:
                if (dpath.parse.last_modified - path_dict[dpath.relative_path]).total_seconds() > 0.01:
                    self.__path_db.collection.find_one_and_update({'_id':path_record['_id']},{'$set':{'last_modified':dpath.parse.last_modified}})
                del path_dict[dpath.relative_path]


            # 插入文件信息
            if len(filenames) > 0:
                for file in filenames:
                    file_record = self.__file_db.collection.find_one({'full_file_name':os.path.join(dpath.relative_path,file)})
                    mfile = PathParse(os.path.join(dirpath,file))
                    if file_record is None:
                        file_tags = mfile.tags
                        #print(mfile.file_name_with_dir)
                        self.__file_db.collection.insert_one({
                            'full_file_name': os.path.join(dpath.relative_path,file),
                            'file_name': mfile.file_name,
                            'directory': self.__path_db.collection.find_one({'path':Path(dirpath,self.__path_name).relative_path})['_id'],
                            'extension': mfile.extension,
                            'last_modified': mfile.last_modified,
                            'size': len(mfile),
                            'author': mfile.author,
                            'time': mfile.time,
                            'version': mfile.version,
                            'tags': file_tags,
                            'project': mfile.project
                        })
                    else:
                        if len(mfile) != file_record['size']:
                            self.__file_db.collection.find_one_and_update({'_id':file_record['_id']},
                                                                          {'$set':{'last_modified':mfile.last_modified,
                                                                                   'size':len(mfile)}})
                        del file_dict[os.path.join(dpath.relative_path,file)]

    def close_db(self):
        self.__path_db.close()
        self.__file_db.close()
        self.__tag_db.close()


if __name__ == '__main__':
    file_path = PathDBupdater('E:\\room\\libs')
    file_path.to_update_path_and_file_db()
    file_path.close_db()
