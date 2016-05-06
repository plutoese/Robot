# coding=UTF-8

import requests
from bs4 import BeautifulSoup

html = requests.get('http://econpapers.repec.org/article/aeaaecrev/')
print(html.status_code)

bsObj = BeautifulSoup(html.text, "lxml")
print(bsObj.h1)











