# coding=UTF-8

# --------------------------------------------------------------
# class_MongoDB文件
# @class: MongoDB类
# @introduction: MongoDB类用来链接Mongodb数据库
# @dependency: pymongo包
# @author: plutoese
# @date: 2016.01.27
# --------------------------------------------------------------

from pymongo import MongoClient


class MongoDB:
    """MongoDB类连接MongoDB数据库进行操作

    :param str host: 数据库主机，默认是'localhost'
    :param int port: 数据库端口，默认是27017
    :return: 无返回值
    """
    def __init__(self, host='localhost', port=27017):
        self.__client = MongoClient(host, port)
        self.__db = None
        self.__collection = None

    def connect(self, database_name, collection_name):
        """连接MongoDB数据中的集合

        :param str database_name: 数据库名称
        :param str collection_name: 集合名称
        :return: 数据集合的连接
        :rtype: pymongo.collection.Collection对象
        """
        if database_name in self.__client.database_names():
            self.__db = self.__client[database_name]
        else:
            print('No such database: ', database_name)
            raise NameError

        if collection_name in self.__db.collection_names():
            self.__collection = self.__db[collection_name]
        else:
            print('No such collection: ', collection_name)
            raise NameError

    def close(self):
        """Disconnect from MongoDB

        :return:
        """
        self.client.close()

    @property
    def client(self):
        return self.__client

    @property
    def database(self):
        return self.__db

    @property
    def collection(self):
        return self.__collection

if __name__ == '__main__':
    db = MongoDB()
    print(db.client.database_names())

