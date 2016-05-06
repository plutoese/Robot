# coding=UTF-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re

webs = json.load(open('d:\\down\\aer_pages.txt'))
#for web in webs[5:7]:
for web in ['http://econpapers.repec.org/article/aeaaecrev/v_3a60_3ay_3a1970_3ai_3a2_3ap_3a403.htm']:
    if re.search('#v\d+',web) is not None:
        continue

    print(web)
    try:
        html = urlopen(web)
        bsObj = BeautifulSoup(html, "lxml")
    except:
        print('Wrong')
    title = str(bsObj.select('.colored')[0])
    print(title)
    print(re.split('<',re.split('>',title)[1])[0])
    #authors = bsObj.find_all(href=re.compile('/RAS/.+'))
    authors = bsObj.select('h1 + p > i')
    print('authors',authors)
    website = bsObj.find(href=re.compile('^/RePEc'))
    print(re.split('<',re.split('>',str(website))[1])[0])
    #print(website)
    for author in authors:
        print(author)
        if re.search('<a href',str(author)) is not None:
            print(re.split('<',re.split('\">',str(author))[1])[0])
        else:
            print(re.split('<',re.split('>',str(author))[1])[0])
    all_p = bsObj.find_all('p')
    for p in all_p:
        if re.search('<p><i>.+American Economic Review',str(p)) is not None:
            print(str(p))
            j_info = re.split('<',re.split('>,',str(p))[1])[0]
            for info in re.split(',',j_info):
                info = re.sub('\s+','',info)
                if re.match('^\d{4}$',info):
                    print(info)
                if re.match('^vol\.\d+$',info):
                    print(re.search('\d+',info).group())
                if re.match('^issue\d+$',info):
                    print(re.search('\d+',info).group())
                if re.match('^pages\d+(-\d+)?$',info):
                    print(re.search('\d+(-\d+)?',info).group())

        if re.search('Abstract',str(p)) is not None:
            print('hello',str(p))
            print(re.split('\s+<',re.split('>\s+',str(p))[1])[0])




