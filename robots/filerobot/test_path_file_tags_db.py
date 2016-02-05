# coding=UTF-8

from libs.database.class_mongodb import MongoDB
from collections import deque

# 1. 连接数据库集合
path_db, file_db, tag_db = MongoDB(), MongoDB(), MongoDB()

path_db.connect('FileIndex','pathdb')
file_db.connect('FileIndex','filedb')
tag_db.connect('FileIndex','tagdb')

# 2. 返回文件夹树
paths = deque(path_db.collection.find({'path':'.'}))
print(paths)

while paths:
    newpath = paths.pop()
    print(newpath['path'])
    paths.extend([path_db.collection.find_one({'_id':item}) for item in reversed(newpath['children_id'])])






















