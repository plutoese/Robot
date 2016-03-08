# coding=UTF-8

# --------------------------------------------------------------
# class_autobrowser文件
# @class: AutoBrowser类
# @introduction: AutoBrowser类用来执行自动化浏览器
# @dependency: urllib包
# @author: plutoese
# @date: 2016.02.23
# --------------------------------------------------------------

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import Select


class AutoBrowser:
    """ AutoBrowser类用来执行自动化浏览器

    :param str proxy: proxy的地址，形式如'58.20.128.123:80'
    :return: 无返回值
    """
    def __init__(self,proxy=None):
        # 设置代理服务器
        if proxy is not None:
            print(proxy)
            self.__proxy = Proxy({'proxyType':ProxyType.MANUAL,
                                  'httpProxy':proxy,
                                  'ftpProxy':proxy,
                                  'sslProxy':proxy,
                                  'noProxy':''})
            self.browser = webdriver.Firefox(proxy=self.__proxy)
        else:
            self.browser = webdriver.Firefox()

        # 最大化浏览器
        self.browser.maximize_window()
        self.pages = dict()
        self.current_window_handle = None
        self.window_handles = None

    def surf(self,website=None,time_out=5):
        """ 浏览某网站

        :param str website: 网站地址
        :param int time_out: 超时设置
        :return: 无返回值
        """
        self.browser.get(website)
        time.sleep(time_out)
        self.pages[self.browser.current_window_handle] = {'url':self.browser.current_url,
                                                          'title':self.browser.title,
                                                          'parent':None}
        self.current_window_handle = self.browser.current_window_handle
        self.window_handles = set(self.browser.window_handles)

    def locate(self,css_selector=None,id=None,xpath=None,link_text=None):
        """ 定位页面元素

        :param str css_selector: css选择器
        :param str id: id选择
        :param str xpath: xpath选择
        :param str link_text: 连接文本
        :return: 返回定位
        :rtype: selenium.webdriver.remote.webelement.WebElement
        """
        if css_selector is not None:
            print(type(self.browser.find_element_by_css_selector(css_selector)))
            return self.browser.find_element_by_css_selector(css_selector)
        if id is not None:
            return self.browser.find_element_by_id(id)
        if xpath is not None:
            return self.browser.find_element_by_xpath(xpath)
        if link_text is not None:
            return self.browser.find_element_by_link_text(link_text)

    def get_text(self,location,beautiful=True):
        """ 返回文本

        :param str,selenium.webdriver.remote.webelement.WebElement location: 网页定位
        :param bool beautiful: 是否返回beautiful soup对象
        :return: 返回页面元素
        :rtype: str, Beautiful soup
        """
        if isinstance(location,str):
            location = self.locate(css_selector=location)

        if beautiful:
            return BeautifulSoup(location.text,'lxml')
        else:
            return location.text

    def interact_one_time(self,location,send_text=None,click=False,select_text=None):
        """ 与页面交互

        :param str,selenium.webdriver.remote.webelement.WebElement location: 页面元素位置
        :param str send_text: 发送文本
        :param bool click: 是否点击
        :param str select_text: 选择文本
        :return: 无返回值
        """
        if isinstance(location,str):
            location = self.locate(css_selector=location)

        if click is True:
            location.click()
        if send_text is not None:
            location.send_keys(send_text)
        if select_text is not None:
            Select(location).select_by_visible_text(select_text)

        tmp_handles = self.browser.window_handles
        handle = tmp_handles[len(tmp_handles) - 1]
        if handle not in self.window_handles:
            self.window_handles.add(handle)
            self.browser.switch_to.window(handle)
            self.pages[handle] = {'url':self.browser.current_url,
                                  'title':self.browser.title,
                                  'parent':self.current_window_handle}
            self.current_window_handle = handle

    def switch(self,iframe=None):
        """ 转换网页框架

        :param str iframe: 网页框架名称
        :return: 无返回值
        """
        if iframe is not None:
            self.browser.switch_to.frame(iframe)

    def switch_to_parent(self,close=True):
        """ 转换到父页面

        :param bool close: 是否关闭子页面
        :return: 无返回值
        """
        parent_handle = self.pages[self.current_window_handle]['parent']
        if close:
            self.window_handles.remove(self.current_window_handle)
            self.close()
        self.browser.switch_to.window(parent_handle)
        self.current_window_handle = parent_handle

    def close(self):
        """ 关闭当前浏览器

        :return: 无返回值
        """
        self.browser.close()

    def quit(self):
        """ 退出浏览器

        :return: 无返回值
        """
        self.browser.quit()

if __name__ == '__main__':
    browser = AutoBrowser(proxy='58.20.128.123:80')
    browser.surf('http://epub.cnki.net/kns/brief/result.aspx?dbprefix=CJFQ')
    browser.interact_one_time(location=browser.locate('.leftinside > ul:nth-child(1) > li:nth-child(1) > p:nth-child(2) > a:nth-child(3)'),click=True)
    print(browser.get_text('.txt0'))
    browser.interact_one_time(location=browser.locate('div.bg_white:nth-child(3) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)'),click=True)
    print(browser.current_window_handle)
    browser.quit()
