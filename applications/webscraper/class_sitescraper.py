# coding=UTF-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json
import pickle

class SiteScraper:
    """用来抓取网站数据

    :param str website: 网页地址
    :return: 无返回值
    """
    def __init__(self,website=None):
        # 设置网站地址
        self.website = website

        # 设置网页地址集合
        self.pages = set()

        # 设置bsobj的列表
        #self.bsobjects = dict()

    def get_links(self,page_url,condition=None):
        """ 获取链接网址

        :param str page_url: 相对网页路径
        :param str condition: 筛选条件
        :return: 无返回值
        """
        html = urlopen(self.website + page_url)
        bsObj = BeautifulSoup(html, "lxml")

        for link in bsObj.findAll("a", href=re.compile(condition)):
            if 'href' in link.attrs:
                if link.attrs['href'] not in self.pages:
                    # We have encountered a new page
                    newPage = link.attrs['href']
                    print(newPage)
                    self.pages.add(newPage)
                    self.get_links(newPage,condition)


if __name__ == '__main__':
    '''
    site_scraper = SiteScraper("http://econpapers.repec.org/article/aeaaecrev/")
    site_scraper.get_links(page_url="",condtion="^(v_|#v|default)")
    site_scraper.export('d:\\down\\aer_pages.txt')'''

    P = json.load(open('d:\\down\\aer_pages.txt'))
    print(len(P))