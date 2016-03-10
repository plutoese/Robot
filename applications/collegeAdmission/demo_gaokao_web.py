# coding=UTF-8

import random
import time
from libs.network.class_autobrowser import AutoBrowser

proxy_list = ['58.22.86.44:8000', '61.179.110.8:8081',
              '110.53.5.250:80',
    '58.246.242.154:8080']

proxy_checked_list = ['58.20.234.243:8000','58.20.242.85:8000',
                      '110.52.232.56:8000','110.52.232.56:80',
                      '58.20.232.239:8000','58.246.242.154:8080',
                      '58.20.232.239:8000','110.52.232.75:8000',
                      '60.13.74.184:81','110.52.232.60:8000',
                      '58.247.30.222:8080','58.22.86.44:8000']

browser = AutoBrowser(proxy=proxy_list[random.randint(0,len(proxy_list)-1)])
browser.surf('http://gkcx.eol.cn/soudaxue/queryProvinceScore.html')
browser.interact_one_time('.gaoxiaoshengyuandi_s > span:nth-child(2) > a:nth-child(1) > img:nth-child(1)',click=True)
browser.interact_one_time('div.tabs_10:nth-child(1)',click=True)
browser.interact_one_time(location=browser.locate(link_text='福建'),click=True)

browser.interact_one_time('.getFstypegaoxiaogesheng_s > span:nth-child(2) > a:nth-child(1) > img:nth-child(1)',click=True)
browser.interact_one_time(location=browser.locate(link_text='文科'),click=True)

browser.interact_one_time('#provinceScoreKEY',send_text='复旦大学')
browser.interact_one_time('#dxlqx > form:nth-child(1) > div:nth-child(2) > input:nth-child(1)',click=True)
time.sleep(5)

print(browser.browser.find_element_by_css_selector('#queryschoolad').text)
u1 = browser.browser.current_url
browser.interact_one_time(location=browser.locate(link_text='下一页'),click=True)
u2 = browser.browser.current_url
time.sleep(10)
print(u1,u2)
print(u1==u2)
browser.interact_one_time(location=browser.locate(link_text='下一页'),click=True)
time.sleep(10)
browser.quit()