# coding=UTF-8

import time
import re
import json
from libs.database.class_mongodb import MongoDB
from bs4 import BeautifulSoup
from libs.network.class_autobrowser import AutoBrowser
from selenium.webdriver.common.by import By

'''
# 设定代理服务器
proxy = '58.133.61.3:3128'

# 设置浏览器
browser = AutoBrowser()
browser.surf('http://epub.cnki.net/kns/oldnavi/n_list.aspx?NaviID=103&Field=%25e6%2595%25b0%25e6%258d%25ae%25e5%25ba%2593%25e5%2588%258a%25e6%25ba%2590&Value=0008%253f&OrderBy=idno&NaviLink=CSSCI+%e4%b8%ad%e6%96%87%e7%a4%be%e4%bc%9a%e7%a7%91%e5%ad%a6%e5%bc%95%e6%96%87%e7%b4%a2%e5%bc%95%ef%bc%882014%e2%80%942015%ef%bc%89%e6%9d%a5%e6%ba%90%e6%9c%9f%e5%88%8a%ef%bc%88%e5%90%ab%e6%89%a9%e5%b1%95%e7%89%88%ef%bc%89%28715%e7%a7%8d%e6%9c%9f%e5%88%8a%29&DisplayMode=%E8%AF%A6%E7%BB%86%E6%96%B9%E5%BC%8F',
             ready_check=(By.CSS_SELECTOR,'#bottom'))

journal = list()
for i in range(1,73):
    browser.interact_one_time(location=browser.locate(id='txtPageGoToBottom'),send_text=str(i))
    browser.interact_one_time(location=browser.locate(id='imgbtnGo'),click=True)

    result = BeautifulSoup(browser.browser.find_element_by_css_selector('#lblList').text,'lxml')
    content = str(result.find_all('p'))
    content = re.split('</p>\]',re.split('\[<p>',content)[1])[0]
    items = re.split('\n',content)
    items = [item for item in items if '：' in item]

    a_journal = dict()
    for item in items:
        name, value = re.split('：',item)
        name = re.sub('\s+','',name)
        if re.match('^被引频次$',name) is not None:
            a_journal['来源'] = u'CSSCI 中文社会科学引文索引（2014—2015）来源期刊（含扩展版）'
            journal.append(a_journal)
            a_journal = dict()
            continue

        if re.match('^英文名称$',name) is not None:
            a_journal[name] = value
            continue

        if re.match('^综合影响因子$',name) is not None:
            a_journal[name] = float(value)
            continue

        if re.match('^复合影响因子$',name) is not None:
            a_journal[name] = float(value)
            continue

        a_journal[name] = re.sub('\s+','',value)

for j in journal:
    print(j)

out_file = r'E:\gitrobot\files\literature\jjournals_cssci.txt'
json.dump(journal, fp=open(out_file,'w'))
browser.quit()

'''

mongo = MongoDB()
mongo.connect('publication','ChineseJournal')

literatures = json.load(open(r'E:\gitrobot\files\literature\journals_cssci.txt'))
for l in literatures:
    print(l)
    #mongo.collection.insert_one(l)
print(len(literatures))

