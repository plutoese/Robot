# coding=UTF-8

# --------------------------------------------------------------
# main_literature_review_one文件
# @goal: 初步文献综述
# @introduction: 自动化文献综述，并生成初步报告
# @process：步骤
# %step 1:
# @date: 2016.02.27
# --------------------------------------------------------------

import json
import random
from applications.literature.class_cnki import Cnki

# 1. 配置初始参数
PROXY_LIST = ['58.20.128.123:80', '36.7.151.29:8000', '61.174.13.12:80',
              '112.90.179.153:4040', '58.20.235.180:8000', '58.22.86.44:8000',
              '101.226.249.237:80', '111.1.89.254:80', '112.16.87.24:80']
QUERY_STRING = "SU='城镇化'*'工资'"
START_PERIOD = "2010"
END_PERIOD = "2016"
SUBJECTS = ["经济与管理科学","社会科学Ⅱ辑"]
LITERATURE_JSON_FILE = r"E:\gitrobot\files\literature\literature_list.txt"

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

    P = json.load(open(LITERATURE_JSON_FILE))
    print('finally, ',len(P))

