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
from selenium import webdriver
from libs.network.class_proxy import Proxy


class AutoBrowser:
    def __init__(self,proxy_dict=None):
        if proxy_dict is not None:
            self.__set_proxy(proxy_dict)
        else:
            self.browser=webdriver.Firefox()



    def __set_proxy(self,proxy_dict):
        """ 设置代理服务器

        :param dict proxy_dict: 代理服务器字典
        :return: 无返回值
        """
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", proxy_dict['address'])
        profile.set_preference("network.proxy.http_port", proxy_dict['port'])
        profile.update_preferences()

        self.browser=webdriver.Firefox(firefox_profile=profile)

if __name__ == '__main__':
    proxy = Proxy(full_address='http://60.191.164.22:3128')
    if proxy.is_valid():
        auto_browser = AutoBrowser(proxy_dict={'address':proxy.address,'port':proxy.port})
        print('I am here!')
    else:
        auto_browser = AutoBrowser()
        print('I am not here!')
    auto_browser.browser.get("http://www.baidu.com")
    auto_browser.browser.maximize_window()
    time.sleep(20)
    auto_browser.browser.quit()
