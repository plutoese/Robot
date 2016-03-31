# coding=UTF-8

# --------------------------------------------------------------
# main_literature_review_one文件
# @goal: 初步文献综述
# @introduction: 自动化文献综述，并生成初步报告
# @process：步骤
# %step 1:
# @date: 2016.02.27
# --------------------------------------------------------------

import re
import json
import random
from applications.literature.class_cnki import Cnki
from libs.database.class_mongodb import MongoDB
from libs.latex.class_article import Article

# 1. 配置初始参数
PROXY_LIST = ['58.20.128.123:80', '36.7.151.29:8000', '61.174.13.12:80',
              '112.90.179.153:4040', '58.20.235.180:8000', '58.22.86.44:8000',
              '101.226.249.237:80', '111.1.89.254:80', '112.16.87.24:80']
PROXY_LIST = ['111.56.13.150:80', '115.159.5.247:8080', '117.136.234.6:843',
              '60.191.179.53:3128', '60.191.163.235:3128', '120.52.73.33:80']
QUERY_STRING = "SU='城市'*'收缩'"
START_PERIOD = "2010"
END_PERIOD = "2016"
SUBJECTS = ["经济与管理科学","社会科学Ⅱ辑"]
LITERATURE_JSON_FILE = r"E:\gitrobot\files\literature\literature_list.txt"
db = MongoDB()
db.connect('publication','ChineseJournal')
journals = db.collection.find({},projection={'_id':0,'期刊名称':1,'复合影响因子':1})
jours = dict([(journal['期刊名称'],journal['复合影响因子']) for journal in journals])
jours_set = jours.keys()

STEP_ONE = False
STEP_TWO = True

# 2. 进行CNKI网站操作
if STEP_ONE:
    cnki_obj = Cnki(PROXY_LIST[random.randint(0,len(PROXY_LIST)-1)])
    cnki_obj.set_query(QUERY_STRING)
    cnki_obj.set_period(start_period=START_PERIOD,end_period=END_PERIOD)
    cnki_obj.set_subject(subjects=SUBJECTS)
    cnki_obj.submit()
    cnki_obj.sort()
    cnki_obj.select_all_literature()
    cnki_obj.child_operation()
    cnki_obj.get_more()

    cnki_obj.export_to_json(file=LITERATURE_JSON_FILE)
    cnki_obj.close()

if STEP_TWO:
    literatures = json.load(open(LITERATURE_JSON_FILE))
    for liter in literatures:
        paper_dict = literatures[liter]
        paper_dict['title'] = liter
        print(paper_dict)
        if paper_dict['journal'] in jours_set:
            paper_dict['rate'] = ''.join([str(jours[paper_dict['journal']]),'-',paper_dict['ISBN/ISSN']])
        else:
            found = False
            for key in jours_set:
                if re.search(paper_dict['journal'],key) is not None:
                    found = True
                    paper_dict['rate'] = ''.join([str(jours[key]),'-',paper_dict['ISBN/ISSN']])
                    break
            if not found:
                paper_dict['rate'] = ''.join(['0-',paper_dict['title']])

    sortable_literatures = dict([(literatures[key]['rate'],literatures[key])for key in literatures])

    replace_word = {'articleTitle':'计量经济学',
                    'arcticleabstract':'摘要'}
    doc = Article(r'E:\latex\template\article_template_02.tex',replace_word)
    for key in sorted(sortable_literatures,reverse=True)[0:10]:
        item = sortable_literatures[key]
        print(key,sortable_literatures[key])
        doc.document.add_section(item['title'],3)
        doc.document.add_list(['---'.join([item['journal'],item['year']])],type=1)
        doc.document.append(item['abstract'])

    doc.document.generate_tex(r'E:\latex\myreport')
    doc.document.generate_pdf(r'E:\latex\myreport')