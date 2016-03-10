# coding=UTF-8

# --------------------------------------------------------------
# class_ceespider文件
# @class: CEESpider类
# @introduction: CEESpider类(College Entrance Examination)用来抓取高考数据
# @dependency: webdriver包
# @author: plutoese
# @date: 2016.02.27
# --------------------------------------------------------------

import re
import pickle
import time
import random
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from libs.network.class_autobrowser import AutoBrowser


class CEESpider:
    """ CEESpider类(College Entrance Examination)用来抓取高考数据

    """
    def __init__(self,proxy=None):
        self.first_region_set = ['安徽','北京','重庆','福建','广东','广西','甘肃','贵州','河北','河南','湖南','湖北','海南','黑龙江']
        self.second_region_set = ['吉林','江苏','江西','辽宁','内蒙古','宁夏','青海']
        self.third_region_set = ['上海','四川','山西','山东','陕西','天津','新疆','西藏','云南','浙江']
        self.college = ''
        self.last_url = ''
        self.current_url = ''
        self.result = []

        self.browser = AutoBrowser(proxy=proxy,timeout=20)
        self.browser.surf('http://gkcx.eol.cn/soudaxue/queryProvinceScore.html',ready_check=(By.LINK_TEXT,'末页'))

    def select_region(self,region):
        """ 选择省份

        :param str region: 省份
        :return: 无返回值
        """
        self.browser.interact_one_time('.gaoxiaoshengyuandi_s > span:nth-child(2) > a:nth-child(1) > img:nth-child(1)',click=True)

        if region in self.first_region_set:
            self.browser.interact_one_time('div.tabs_10:nth-child(1)',click=True)
        if region in self.second_region_set:
            self.browser.interact_one_time('div.tabs_10:nth-child(2)',click=True)
        if region in self.third_region_set:
            self.browser.interact_one_time('div.tabs_10:nth-child(3)',click=True)

        self.browser.interact_one_time(location=self.browser.locate(link_text=region),click=True)

    def select_subject(self,subject='文科'):
        """ 选择文理科

        :param str subject: 科目，文科或者理科
        :return: 无返回值
        """
        self.browser.interact_one_time('.getFstypegaoxiaogesheng_s > span:nth-child(2) > a:nth-child(1) > img:nth-child(1)',click=True)
        self.browser.interact_one_time(location=self.browser.locate(link_text=subject),click=True)

    def set_college(self,college='复旦大学'):
        """ 设定学校

        :param str college: 学校名称
        :return: 无返回值
        """
        self.college = college
        self.browser.interact_one_time('#provinceScoreKEY',send_text=college)

    def do_search(self):
        """ 开始搜索

        :return: 无返回值
        """
        self.browser.interact_one_time('#dxlqx > form:nth-child(1) > div:nth-child(2) > input:nth-child(1)',click=True)
        if self.browser.is_ready(locator=(By.CSS_SELECTOR,''.join(['td > a[title="',self.college,'"]']))):
            self.current_url = self.browser.browser.current_url
        else:
            raise TimeoutError

    def get_result_and_more(self):
        """ 添加所有页结果到self.result

        :return:
        """
        self.result.append(self.browser.get_text(location='#queryschoolad',beautiful=False))

        self.last_url = self.current_url
        self.browser.interact_one_time(location=self.browser.locate(link_text='下一页'),click=True)
        if self.browser.is_ready(locator=(By.CSS_SELECTOR,''.join(['td > a[title="',self.college,'"]']))):
            self.current_url = self.browser.browser.current_url

            while self.last_url != self.current_url:
                self.result.append(self.browser.get_text(location='#queryschoolad',beautiful=False))
                self.last_url = self.current_url
                self.browser.interact_one_time(location=self.browser.locate(link_text='下一页'),click=True)
                if self.browser.is_ready(locator=(By.CSS_SELECTOR,''.join(['td > a[title="',self.college,'"]']))):
                   self.current_url = self.browser.browser.current_url

    @property
    def colleges(self):
        """ 返回爬虫的结果

        :return: 结果列表
        :rtype: list
        """
        vars = ['university','student_region','subject','year','batch','average_score','province_control_score']
        colleges = []
        for cstr in self.result:
            for item in re.split('\n',cstr)[1:]:
                colleges.append(dict(zip(vars,re.split('\s+',item)[0:8])))

        for item in colleges:
            if re.match('^--$',item['average_score']) is not None:
                item['average_score'] = None
            else:
                item['average_score'] = int(item['average_score'])
            if re.match('^--$',item['province_control_score']) is not None:
                item['province_control_score'] = None
            else:
                item['province_control_score'] = int(item['province_control_score'])

        return colleges

    def close(self):
        """ 关闭浏览器

        :return: 无返回值
        """
        self.browser.quit()

if __name__ == '__main__':
    spider = CEESpider(proxy='58.20.242.85:8000')
    spider.select_region('浙江')
    spider.select_subject()
    spider.set_college()
    spider.do_search()
    spider.get_result_and_more()
    print(spider.colleges)

    #fp = open(r'E:\gitrobot\files\college\exam\college_list.pkl','wb')
    #pickle.dump(spider.colleges, file=fp)
    #fp.close()
    time.sleep(2)
    spider.close()