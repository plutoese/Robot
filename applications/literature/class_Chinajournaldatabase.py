# coding=UTF-8

# --------------------------------------------------------------
# class_Chinajournaldatabase文件
# @class: ChinaJournalDatabase类
# @introduction: ChinaJournalDatabase类用来连接中文文献数据库
# @dependency: MongoDB类
# @author: plutoese
# @date: 2016.03.23
# --------------------------------------------------------------

from libs.database.class_mongodb import MongoDB


class ChinaJournalDatabase:
    """ ChinaJournalDatabase类用来连接中文文献数据库

    """
    def __init__(self,proxy=None):
        self.mongo = MongoDB()
        self.mongo.connect('publication','ChineseJournal')
        self.collection = self.mongo.collection

    def getByName(self,journal_name=None,exactly=False,auto=False):
        if auto:
            result = list(self.find(condition={'中文名称':journal_name}))
            if len(list(result)) < 1:
                result = list(self.find(condition={'中文名称':{'$regex':journal_name}}))
            return result
        else:
            if exactly:
                return list(self.find(condition={'中文名称':journal_name}))
            else:
                return list(self.find(condition={'中文名称':{'$regex':journal_name}}))

    def find(self,condition=None):
        """ 查询

        :param dict condition: 查询条件
        :return: 查询结果
        """
        return self.collection.find(condition)

    def close(self):
        """ 关闭数据库连接

        :return: 无返回值
        """
        self.mongo.close()


if __name__ == '__main__':
    jounal_db = ChinaJournalDatabase()
    #jounal_db.find(condition={'中文名称':{'$regex':'经济学'}})
    for j in jounal_db.getByName('浙江金融'):
        print(j['中文名称'])

    jounal_db.close()
