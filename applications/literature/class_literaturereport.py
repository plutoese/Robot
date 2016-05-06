# coding=UTF-8

# --------------------------------------------------------------
# class_literaturereport文件
# @class: LiteratureReport类
# @introduction: LiteratureReport类生成初步文献报告
# @dependency: urllib包，bs4包
# @author: plutoese
# @date: 2016.04.08
# --------------------------------------------------------------

import json
from libs.database.class_mongodb import MongoDB
from pymongo import ASCENDING, DESCENDING
from libs.latex.class_article import Article


class LiteratureReport:
    def __init__(self,database=None,collection=None,file=None):
        self.literatures = None
        if database is not None:
            self.mongo = MongoDB()
            self.mongo.connect(database,collection)

        if file is not None:
            self.literatures = json.load(open(file))

    def load_record_from_db(self,query=None,sort=None):
        if query is None:
            self.literatures = self.mongo.collection.find({})
        else:
            if sort is None:
                self.literatures = self.mongo.collection.find(query)
            else:
                self.literatures = self.mongo.collection.find(query).sort(sort)

    def to_report(self):
        replace_word = {'articleTitle':'Literature Report',
                    'arcticleabstract':'Abstract'}
        doc = Article(r'E:\latex\template\article_template_02.tex',replace_word)
        for item in self.literatures:
            doc.document.add_section(item['title'],3)
            doc.document.add_list(['---'.join([item['journal'],item['year'],item['vol'],item['issue']])],type=1)
            abstract = item.get('abstract')
            if abstract is not None:
                doc.document.append(abstract)
        doc.document.generate_tex(r'E:\latex\journalreport')
        doc.document.generate_pdf(r'E:\latex\journalreport')


if __name__ == '__main__':
    report = LiteratureReport(database='paper',collection='literature')
    report.load_record_from_db(query={'year':{'$gte':'2014'}},
                               sort=[('journal',ASCENDING),('year',DESCENDING)])
    report.to_report()
