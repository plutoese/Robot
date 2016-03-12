# coding=UTF-8

# --------------------------------------------------------------—————————————————
# class_ceespidersina文件
# @class: CEESpiderSina类
# @introduction: CEESpiderSina类(College Entrance Examination)用来抓取高考数据，数据来源于新浪高考
# @dependency: webdriver包
# @author: plutoese
# @date: 2016.02.27
# --------------------------------------------------------------—————————————————

import re
import pickle
import time
import random
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from libs.network.class_autobrowser import AutoBrowser


class CEESpiderSina:
    """ CEESpiderSina类(College Entrance Examination)用来抓取高考数据，数据来源于新浪高考

    """
    def __init__(self,proxy=None):
        self.region = ''
        self.result = []

        self.browser = AutoBrowser(proxy=proxy,timeout=20)
        self.browser.surf('http://kaoshi.edu.sina.com.cn/college/collegeAvgScoreRank?syear=2013&provid=1',ready_check=(By.CLASS_NAME,'pageNumWrap'))

    def select_region(self,region):
        """ 选择省份

        :param str region: 省份
        :return: 无返回值
        """
        self.region = region
        self.browser.interact_one_time('#provSel',select_text=region)


    def select_subject(self,subject='文科'):
        """ 选择文理科

        :param str subject: 科目，文科或者理科
        :return: 无返回值
        """
        self.browser.interact_one_time('#typeSel',select_text=subject)

    def select_year(self,year='2014'):
        """ 选择年份

        :param str year: 年份
        :return: 无返回值
        """
        self.browser.interact_one_time('#sYear',select_text=year)

    def select_batch(self,batch='本科一批'):
        """ 选择批次

        :param str order: 批次
        :return: 无返回值
        """
        self.browser.interact_one_time('#sBatch',select_text=batch)

    def do_search(self):
        """ 开始搜索

        :return: 无返回值
        """
        self.browser.interact_one_time('#searchBtn',click=True)

        if self.browser.is_ready(locator=(By.CLASS_NAME,'pageNumWrap')):
            self.current_url = self.browser.browser.current_url
        else:
            raise TimeoutError
        time.sleep(5)

    def clear(self):
        """ 清空结果

        :return:
        """
        self.result = []

    def get_result_and_more(self):
        """ 添加所有页结果到self.result

        :return:
        """
        is_next = True
        self.result.append(self.browser.get_text(location='#scoreTable2',beautiful=False))

        while(is_next):
            try:
                self.browser.browser.find_element_by_css_selector('.pageNumWrap > [node-type="next"]')
                self.browser.interact_one_time('.pageNumWrap > [node-type="next"]',click=True)
                time.sleep(2)
                if not self.browser.is_ready(locator=(By.CLASS_NAME,'pageNumWrap')):
                    raise TimeoutError
                self.result.append(self.browser.get_text(location='#scoreTable2',beautiful=False))
            except NoSuchElementException:
                break

    @property
    def colleges(self):
        """ 返回爬虫的结果

        :return: 结果列表
        :rtype: list
        """
        vars = ['university','type','university_region','average_score','subject','year','batch','student_region']
        colleges = []
        for cstr in self.result:
            for item in re.split('\n',cstr):
                new_item = re.split('\s+',item)[1:8]
                new_item.append(self.region)
                colleges.append(dict(zip(vars,new_item)))

        colleges = [item for item in colleges if len(item) > 7]

        '''
        for item in colleges:
            if re.match('^--$',item['average_score']) is not None:
                item['average_score'] = None
            else:
                item['average_score'] = int(float(item['average_score']))
            if re.match('^--$',item['province_control_score']) is not None:
                item['province_control_score'] = None
            else:
                item['province_control_score'] = int(float(item['province_control_score']))'''

        return colleges

    def close(self):
        """ 关闭浏览器

        :return: 无返回值
        """
        self.browser.quit()

if __name__ == '__main__':
    spider = CEESpiderSina()
    spider.select_region('宁夏')
    spider.select_subject('文科')
    spider.select_year('2014')
    spider.select_batch('本科三批')
    spider.do_search()
    spider.get_result_and_more()
    print(spider.colleges)
    print(len(spider.colleges))
    time.sleep(10)
    spider.close()