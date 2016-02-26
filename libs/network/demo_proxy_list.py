# coding=UTF-8

from urllib import request
from bs4 import BeautifulSoup
import re
import requests

web_address = 'http://www.youdaili.net/Daili/guonei/'
firset_web = request.urlopen(web_address)

bsObj = BeautifulSoup(firset_web, "lxml")
result1 = bsObj.find(class_='newslist_line')
proxy_web = result1.find('a').attrs['href']

secord_web = request.urlopen(proxy_web)
r = requests.get(proxy_web)
print(r.encoding)
r.encoding = 'utf-8'
print(r.text)
bsObj = BeautifulSoup(r.text, "lxml")

ip_address = bsObj.find_all(text=re.compile('\d+\.\d+\.\d+\.\d+'))


for ip in ip_address:
    print(re.split('@',re.sub('\s+','',ip)))

