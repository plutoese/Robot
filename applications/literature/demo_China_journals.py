# coding=UTF-8

import time
import re
import json
import random
from libs.database.class_mongodb import MongoDB
from bs4 import BeautifulSoup
from libs.network.class_autobrowser import AutoBrowser
from selenium.webdriver.common.by import By
from libs.file.class_Excel import Excel
from bson.objectid import ObjectId

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
'''
literatures = json.load(open(r'E:\gitrobot\files\literature\journals_cssci.txt'))
for l in literatures:
    print(l)
    #mongo.collection.insert_one(l)
print(len(literatures))'''

proxy_list = ['101.26.38.162:82']
proxy_list = ['111.56.13.152:80', '101.26.38.162:80', '101.26.38.162:82', '111.56.13.150:80', '60.191.157.155:3128', '60.191.175.54:3128', '60.191.167.93:3128', '61.163.32.6:3128', '49.1.244.139:3128', '112.16.76.188:8080', '60.191.163.147:3128', '60.194.100.51:80', '101.226.12.223:80', '82.200.81.233:80', '85.143.24.70:80', '59.58.162.141:888', '110.18.241.9:3128', '60.15.41.214:3128', '61.7.149.69:8080', '61.184.199.203:3128', '86.100.118.44:81', '61.150.89.67:3128', '61.162.223.41:9797', '95.168.217.24:3128', '86.100.118.44:80', '31.173.74.73:8080', '58.248.137.228:80', '79.120.72.222:3128', '46.218.85.101:3129', '106.56.225.200:3128', '60.15.55.228:3128', '60.13.74.184:81', '101.200.234.114:8080', '104.238.83.28:443', '91.183.124.41:80', '60.191.164.22:3128', '62.204.241.146:8000', '60.191.174.227:3128', '60.191.153.12:3128', '61.53.65.52:3128', '36.250.69.4:80', '61.153.198.178:3128', '60.191.153.75:3128', '60.191.178.43:3128', '60.13.74.184:82', '60.13.74.184:80', '60.191.161.244:3128', '60.191.170.122:3128', '60.191.167.11:3128', '61.175.220.4:3128', '61.164.92.254:9999', '61.75.2.124:3128', '27.122.12.45:3128', '64.62.233.67:80', '113.140.43.51:3128', '60.191.166.130:3128', '113.107.57.76:8101', '113.107.57.76:80', '60.191.160.20:3128', '61.134.34.148:3128', '93.51.247.104:80', '60.191.164.59:3128', '91.142.84.182:3128', '72.252.11.91:8080', '59.44.244.14:9797', '58.18.50.10:3128', '58.96.187.208:3128', '85.194.75.18:8080', '113.105.80.61:3128', '58.59.141.187:3128', '61.163.45.240:3128', '91.108.131.250:8080', '110.17.172.150:3128']
#browser = AutoBrowser(proxy=proxy_list[random.randint(0,len(proxy_list)-1)])
#browser = AutoBrowser(proxy='101.26.38.162:82')
browser = AutoBrowser()
browser.surf('http://navi.cnki.net/knavi/journal/Detailq/CJFD/JJYJ?Year=&Issue=&Entry=',
             ready_check=(By.CSS_SELECTOR,'#bottom'))

result = []
for item in mongo.collection.find({'ISSN':None}):
    print(item['中文名称'])
    browser.interact_one_time(location=browser.locate(id='navi-search-value'),send_text=item['中文名称'])
    browser.interact_one_time(location=browser.locate(id='navi-search-button'),click=True)
    time.sleep(2)
    browser.interact_one_time(location=browser.locate(
            css_selector=''.join(['a[title="',item['中文名称'],'"]'])),click=True)
    time.sleep(2)
    data = BeautifulSoup(browser.browser.find_element_by_css_selector('.list01').text,"lxml")
    ISSN = re.search('\d{4}-\d{3}[0-9a-zA-Z]',str(data)).group()
    print(ISSN)
    mongo.collection.update_one({'_id': item['_id']}, {'$set':{'ISSN':ISSN}})
    result.append({'journal':item['_id'],'ISSN':ISSN})
    #browser.interact_one_time(location=browser.locate(css_selector='#lblNaviName > a:nth-child(1)'),click=True)
    time.sleep(1)

browser.quit()
out_file = r'E:\gitrobot\files\literature\Chinese_journal_issn.txt'
json.dump(result, fp=open(out_file,'w'))

'''
file = r'D:\down\demo.xlsx'
mdata = Excel(file).read()

for item in mdata:
    mongo.collection.update_one({'_id': ObjectId(item[0])}, {'$set':{'ISSN':item[2]}})'''
