# coding=UTF-8

# --------------------------------------------------------------
# class_econpapers文件
# @class: EconPapersSiteScraper类
# @introduction: EconPapers类获取和解析EconPapers网站内容
# @dependency: urllib包，bs4包
# @author: plutoese
# @date: 2016.04.08
# --------------------------------------------------------------

from urllib.request import urlopen, HTTPError
from bs4 import BeautifulSoup
import json
import re
from applications.webscraper.class_sitescraper import SiteScraper
from libs.database.class_mongodb import MongoDB


class EconPapers:
    """ EconPapers类获取和解析EconPapers网站内容

    :param str journal_web: 杂志首页
    :return: 无返回值
    """
    def __init__(self,journal=None,journal_web=None):
        self.journal_web = journal_web
        self.scraper = SiteScraper(journal_web)
        # 期刊名称
        self.journal = journal
        # 网页集合
        self.literature_websites = None
        # 文献信息列表
        self.literature_info = list()

    def to_literature_websites(self,condition=None,filter=None):
        """ 构建文献网址的列表

        :param str condition: 筛选条件
        :param str filter: 过滤条件
        :return: 无返回值
        """
        self.scraper.get_links(page_url="",condition=condition)
        pages = self.scraper.pages

        if filter is not None:
            pages = (page for page in pages if re.search(filter,page) is not None)

        self.literature_websites = [''.join([self.journal_web,page]) for page in pages]

    def get_literature_info(self,websites=None):
        """ 利用网页信息获取文献信息

        :param str,list websites: 网页地址
        :return: 无返回值
        """
        if websites is None:
            websites = self.literature_websites

        if isinstance(websites,str):
            websites = [websites]

        i = 0
        for web in websites:
            print(i)
            econ_parser = EconPapersLitPageParser(page=web,journal=self.journal)
            self.literature_info.append(econ_parser.literature_info)
            i += 1

    def export_literature_websites(self,file):
        """ 导出文献网址

        :param str file: 导出的文件名
        :return: 无返回值
        """
        json.dump(self.literature_websites, fp=open(file,'w'))


class EconPapersLitPageParser:
    def __init__(self,page,journal):
        print(page)
        self.journal = journal
        self.ISSN = self.get_ISSN_from_journal()
        self.page = page
        self.literature_info = dict()
        self._parser()

    def get_ISSN_from_journal(self,auto=True):
        mongo = MongoDB()
        mongo.connect('publication','WesternJournal')
        if auto:
            result = list(mongo.collection.find({'journal':self.journal.upper()}))
            if len(result) < 1:
                result = list(mongo.collection.find({'journal':{'$regex':self.journal.upper()}}))
            if len(result) < 1:
                return None
            else:
                ISSN = result[0]['SSIN']
                return ISSN
        else:
            result = list(mongo.collection.find({'journal':self.journal.upper()}))
            if len(result) < 1:
                return None
            else:
                ISSN = result[0]['SSIN']
                return ISSN

    def _parser(self):
        try:
            html = urlopen(self.page)
            bsObj = BeautifulSoup(html, "lxml")

            # 文献隶属杂志
            self.literature_info['journal'] = self.journal

            if self.ISSN is not None:
                self.literature_info['ISSN'] = self.ISSN

            # 文献标题
            self.literature_info['title'] = re.split('<',re.split('>',str(bsObj.select('.colored')[0]))[1])[0]

            # 文献网址
            self.literature_info['econpapers_web'] = re.split('<',re.split('>',str(bsObj.find(href=re.compile('^/RePEc'))))[1])[0]

            # 作者
            authors = []
            for author in bsObj.select('h1 + p > i'):
                if re.search('<a href',str(author)) is not None:
                    authors.append(re.split('<',re.split('\">',str(author))[1])[0])
                else:
                    authors.append(re.split('<',re.split('>',str(author))[1])[0])
            self.literature_info['author'] = authors

            all_p = bsObj.find_all('p')
            for p in all_p:
                if re.search(''.join(['<p><i>.+',self.journal]),str(p)) is not None:
                    j_info = re.split('<',re.split('>,',str(p))[1])[0]
                    for info in re.split(',',j_info):
                        info = re.sub('\s+','',info)
                        if re.match('^\d{4}$',info):
                            self.literature_info['year'] = info
                        if re.match('^vol\.\d+$',info):
                            self.literature_info['vol'] = re.search('\d+',info).group()
                        if re.match('^issue\d+$',info):
                            self.literature_info['issue'] = re.search('\d+',info).group()
                        if re.match('^pages\d+(-\d+)?$',info):
                            self.literature_info['pages'] = re.search('\d+(-\d+)?',info).group()

                if re.search('Abstract',str(p)) is not None:
                    self.literature_info['abstract'] = re.split('\s+<',re.split('>\s+',str(p))[1])[0]

                if re.search('Keywords',str(p)) is not None:
                    content = re.split('<br/>',str(p))[0]
                    self.literature_info['keyword'] = [re.split('>',re.split('</a>',str(item))[0])[1] for item in BeautifulSoup(content,'lxml').find_all('a')]

        except HTTPError:
            self.literature_info = None

if __name__ == '__main__':

    escraper = EconPapers(journal='Econometrica',
                          journal_web='http://econpapers.repec.org/article/wlyemetrp/')
    '''
    escraper.to_literature_websites(condition="^(v_3a[6-9]\d|#v|default)",filter="^v_")
    #escraper.to_literature_websites(condition="^(v_3|#v|default)",filter="^v_")
    escraper.export_literature_websites(file='d:\\down\\journalofeconometrics_valid_pagesbelow100.txt')

    '''
    webs = json.load(open('d:\\down\\Econometrica_valid_pages.txt'))
    #print(len(webs))


    escraper.get_literature_info(webs[2600:])

    mon = MongoDB()
    mon.connect('paper','literature')
    for linfo in escraper.literature_info:
        print(linfo)
        mon.collection.insert_one(linfo)









