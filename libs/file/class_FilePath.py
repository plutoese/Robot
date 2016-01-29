# coding=UTF-8

# --------------------------------------------------------------
# class_FilePath文件
# @class: FilePath
# @introduction: FilePath类用来处理文件夹
# @dependency: os, os.path包
# @author: plutoese
# @date: 2016.01.28
# --------------------------------------------------------------

import os
import uuid
import re
from collections import OrderedDict


class FilePath:
    """FilePath类用来处理文件夹

    """
    def __init__(self, file_path):
        if os.path.isdir(file_path):
            self.__file_path = file_path
        else:
            print('{} is not a directory!'.format(file_path))
            raise FileNotFoundError

        self.__files = None
        self.__walker = os.walk(self.__file_path)
        self.__path_dict, self.__file_dict = self.__walk_and_record()

    def __walk_and_record(self):
        """遍历目录生成记录

        :return:
        """
        path_dict = OrderedDict({'.': {'_id':uuid.uuid1(),
                                       'relative_path':'',
                                       'parent_path_id':''
                                       }})
        file_dict = OrderedDict()

        for base_path,path,files in self.__walker:
            print(base_path, ' ---> ', path, '===>', files)
            print(os.path.relpath(base_path,self.__file_path))
            # relative_path是相对路径
            relative_path = os.path.relpath(base_path,self.__file_path)

            # 若该目录下有子目录，则提取子目录
            if len(path) > 0:
                if relative_path in path_dict:
                    if re.match('\.',relative_path) is not None:
                        [path_dict.update({item_path: {'_id':uuid.uuid1(),
                                                       'relative_path':item_path,
                                                       'parent_path_id':path_dict.get('.')['_id']}})
                         for item_path in path]
                        path_dict.get(relative_path).update({'children_path_id':[path_dict.get(cpath)['_id'] for cpath in path]})

                    else:
                        [path_dict.update({os.path.join(relative_path,item_path): {'_id':uuid.uuid1(),
                                                                                   'relative_path':os.path.join(relative_path,item_path),
                                                                                   'parent_path_id':path_dict.get(relative_path)['_id']}})
                         for item_path in path]
                        path_dict.get(relative_path).update({'children_path_id':[path_dict.get(os.path.join(relative_path,cpath))['_id'] for cpath in path]})


                # 如果相对路径没有在path_dict的key里，那么报错
                else:
                    print('Wrong! It is not in the dictionary.')
                    raise IndexError

            # 如果目录下有文件，则进行文件归档操作
            if len(files) > 0:
                if re.match('\.',relative_path) is not None:
                    [file_dict.update({file:{'file_name':file,
                                             'relative_path_id':path_dict.get('.')['_id'],
                                             'relative_path_file_name':file}})
                     for file in files]
                else:
                    [file_dict.update({os.path.join(relative_path,file):{'file_name':file,
                                                                         'relative_path_id':path_dict.get(relative_path)['_id'],
                                                                         'relative_path_file_name':os.path.join(relative_path,file)}})
                     for file in files]

        return path_dict, file_dict

    # 打印目录树
    def diretory_tree(self,root='.'):
        print(root)
        for item in self.path_dict.get(root).get('children_path_id'):
            print(item)
            self.diretory_tree()


    @property
    def path_dict(self):
        return self.__path_dict

    @property
    def file_dict(self):
        return self.__file_dict

if __name__ == '__main__':
    file_path = FilePath('E:\\piles')
    print(file_path.path_dict)
    print(file_path.file_dict)
    print('*********************************')
    file_path.diretory_tree()








