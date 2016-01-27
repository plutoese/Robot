

from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pickle
import requests
import re

'''
PhantomJS_path = 'D:/software/phantomjs-2.0.0-windows/bin/phantomjs'
DRIVER = webdriver.PhantomJS(executable_path=PhantomJS_path)

url_load = 'http://gkcx.eol.cn/soudaxue/queryProvinceScore.html?page=2&argprovince=安徽&fstype=文科&scoreSign=3&keyWordForQueryparamsarraycore=安徽师范大学'
DRIVER.get(url_load)
time.sleep(20)
table_data = DRIVER.find_element_by_id("queryschoolad").text
print(table_data)'''

# coding = utf-8
from selenium import webdriver
browser = webdriver.Firefox()
browser.get("http://gkcx.eol.cn/soudaxue/queryProvinceScore.html")
browser.maximize_window()
time.sleep(5)
m = browser.find_element_by_id("Tabs_10")
browser.find_element_by_id("provinceScoreKEY").send_keys("安徽师范大学")
forms = browser.find_element_by_tag_name('form')
browser.find_element_by_xpath("//form[@action='/soudaxue/queryProvinceScore.html']").submit()
time.sleep(10)
#browser.find_element_by_id("su").click()
#time.sleep(20)
table_data = browser.find_element_by_id("queryschoolad").text
print(table_data)
print(browser.current_url)
url2 = re.sub('page=1','page=2',browser.current_url)
browser.get(url2)
time.sleep(10)
url3 = re.sub('page=1','page=2',browser.current_url)
browser.get(url3)
time.sleep(10)
browser.quit()



