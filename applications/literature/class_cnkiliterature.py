# coding=UTF-8

# --------------------------------------------------------------
# class_cnkiliterature文件
# @class: CnkiLiterature类
# @introduction: CnkiLiterature类用来自动化cnki文献搜索
# @dependency: Cnki类
# @author: plutoese
# @date: 2016.03.23
# --------------------------------------------------------------

import json
from applications.literature.class_cnki import Cnki
from applications.literature.class_Chinajournaldatabase import ChinaJournalDatabase


class CnkiLiterature:
    """ CnkiLiterature类用来自动化cnki文献搜索

    """
    def __init__(self,proxy=None):
        self.__jounal_db = ChinaJournalDatabase()
        self.__literatrues = None
        if proxy is None:
            self.cnki_obj = Cnki()
        else:
            self.cnki_obj = Cnki(proxy=proxy)

    def query(self,query_str=None,start_period=None,end_period=None,sort_by='被引',
              limit=4,subjects=['经济与管理科学']):
        """ 查询

        :param str query_str: 查询字符串
        :param str start_period: 起始年份
        :param str end_period: 终止年份
        :param str sort_by: 排序
        :param int limit: 搜索限制数
        :param list subjects: 学科
        :return: 无返回值
        """
        # 设定查询字符串
        self.cnki_obj.set_query(query_str)
        # 设定起始日期
        self.cnki_obj.set_period(start_period=start_period,end_period=end_period)
        # 设定领域
        self.cnki_obj.set_subject(subjects=subjects)
        # 确定搜索
        self.cnki_obj.submit()
        # 排序
        self.cnki_obj.sort(by=sort_by)
        # 选择所有的文献
        self.cnki_obj.select_all_literature()
        # 后续操作
        self.cnki_obj.child_operation()
        # 更多的文献
        self.cnki_obj.get_more(limit=limit)

        self.__literatrues = self.cnki_obj.export_to_dict()

    def sort_by(self,by=None):
        """ 对查询结果排序

        :param str by: 排序根据
        :return: 无返回值
        """
        for item in self.__literatrues:
            paper = self.__literatrues[item]
            paper['title'] = item
            journal = self.__jounal_db.getByName(journal_name=paper['journal'],auto=True)
            if len(journal) < 1:
                paper['rate'] = '---'.join(['0',paper['title']])
            else:
                paper['rate'] = '---'.join([str(journal[0][by]),paper['title']])

        tmp_result = dict([(self.__literatrues[item]['rate'],self.__literatrues[item])
                          for item in self.__literatrues])
        for key in tmp_result:
            del tmp_result[key]['rate']
        self.__literatrues = [tmp_result[item] for item in sorted(tmp_result,reverse=True)]

    @property
    def literatrues(self):
        return self.__literatrues

    def close(self):
        """ 关闭浏览器

        :return: 无返回值
        """
        self.cnki_obj.close()

if __name__ == '__main__':
    '''
    mcnki = CnkiLiterature(proxy='117.177.250.152:8080')
    QUERY_STRING = "SU='城市化'*'收入差距'"
    START_PERIOD = "2012"

    mcnki.query(query_str=QUERY_STRING,start_period=START_PERIOD,limit=2)
    mcnki.sort_by('复合影响因子')
    out_file = r'E:\gitrobot\files\literature\demo_literature_data.txt'
    json.dump(mcnki.literatrues, fp=open(out_file,'w'))
    print(mcnki.literatrues)
    mcnki.close()
    '''
    jounal_db = ChinaJournalDatabase()
    papers = json.load(open(r'E:\gitrobot\files\literature\demo_literature_data.txt'))
    for item in papers:
        paper = papers[item]
        paper['title'] = item
        journal = jounal_db.getByName(journal_name=paper['journal'],auto=True)
        if len(journal) < 1:
            paper['rate'] = '---'.join(['0',paper['title']])
        else:
            paper['rate'] = '---'.join([str(journal[0]['复合影响因子']),paper['title']])

    sortable_literatures = dict([(papers[item]['rate'],papers[item]) for item in papers])
    for p in sorted(sortable_literatures,reverse=True):
        del sortable_literatures[p]['rate']
        print(p,sortable_literatures[p])

