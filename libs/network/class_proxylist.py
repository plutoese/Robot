# coding=UTF-8

# --------------------------------------------------------------
# class_proxylist文件
# @class: ProxyList类
# @introduction: ProxyList类用来生成有效的代理服务器列表
# @dependency: urllib包
# @author: plutoese
# @date: 2016.02.23
# --------------------------------------------------------------

from bs4 import BeautifulSoup
import re
import requests
from libs.network.class_proxy import Proxy
import pickle
from libs.network.class_multithread import MultiThread


class ProxyList:
    """ ProxyList类用来生成有效的代理服务器列表

    :param str proxy_web: proxy的地址，默认为http://www.youdaili.net/Daili/guonei/
    :return: 无返回值
    """
    def __init__(self,proxy_web='http://www.youdaili.net/Daili/guonei/'):
        self.__proxy_web = proxy_web
        self.__proxy_unchecked_list = self._parse()
        self.__proxy_checked_list = list()

    def export(self,file=r'E:\gitrobot\files\proxy\proxy_list.pkl'):
        """ 到处有效的代理服务器列表到文件

        :param str file: 文件名
        :return: 无返回值
        """
        F = open(file, 'wb')
        pickle.dump(self.proxy_checked_list, F)
        F.close()

    def _parse(self):
        """ 辅助函数，用来抓取网站上的代理服务器列表

        :return: 代理服务器列表
        :rtype: list
        """
        first_web = requests.get(self.__proxy_web)
        bsobj_first_web = BeautifulSoup(first_web.text, "lxml")
        result1 = bsobj_first_web.find(class_='newslist_line')
        proxy_web = result1.find('a').attrs['href']

        r = requests.get(proxy_web)
        r.encoding = 'utf-8'
        bsobj_second_web = BeautifulSoup(r.text, "lxml")

        ip_address_list = bsobj_second_web.find_all(text=re.compile('\d+\.\d+\.\d+\.\d+'))
        proxy_list = [re.split('@',re.sub('\s+','',ip))[0] for ip in ip_address_list]
        return proxy_list

    def _check_and_put_proxy(self,ip_address):
        """ 辅助函数，用来检验代理服务器的有效性

        :param str ip_address: 代理服务器地址，形如13.24.22.34:8080
        :return: 无返回值
        """
        if Proxy(''.join(['http://',ip_address])).is_valid():
            print('successful: ',ip_address)
            self.__proxy_checked_list.append(ip_address)

    def multi_thread_check_proxy(self):
        """ 多线程验证代理服务器的有效性，调用辅助函数self._check_and_put_proxy

        :return: 无返回值
        """
        threads = []
        for ip in self.__proxy_unchecked_list:
            t = MultiThread(self._check_and_put_proxy,args=(ip,),name=ip)
            threads.append(t)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    @property
    def proxy_checked_list(self):
        """ 返回有效的代理服务器列表

        :return: 返回有效的代理服务器列表
        :rtype: list
        """
        self.multi_thread_check_proxy()
        return self.__proxy_checked_list

    @property
    def proxy_unchecked_list(self):
        """ 返回网络抓取的代理服务器列表

        :return: 返回网络抓取的代理服务器列表
        :rtype: list
        """
        return self.__proxy_unchecked_list

if __name__ == '__main__':
    plist = ProxyList()
    print(plist.proxy_unchecked_list)
    print(plist.proxy_checked_list)

    '''
    plist.export()

    F = open(r'E:\gitrobot\files\proxy\proxy_list.pkl', 'rb')
    proxy_list = pickle.load(F)
    print('finally, ',proxy_list)'''