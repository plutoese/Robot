# coding=UTF-8

# --------------------------------------------------------------
# class_iptools文件
# @class: IPTools类
# @introduction: IPTools类用来查询及处理ip
# @dependency: urllib包
# @author: plutoese
# @date: 2016.02.23
# --------------------------------------------------------------

from urllib import request
import re
import json
import socket


class IPTools:
    def __init__(self,ip_address=None):
        self.__ip_address = ip_address

    def ip_belong(self,ip=None):
        """ 返回ip归属地

        :param str ip: ip地址
        :return: 返回ip归属地
        :rtype: dict
        """
        if ip is None:
            ip = self.__ip_address
        url = ''.join(['http://ip.taobao.com/service/getIpInfo.php?ip=',ip])
        jsondata = json.loads(request.urlopen(url).read().decode('utf-8'))

        if jsondata['code'] == 1:
            print(jsondata.get('data'))
            return None

        return {'country':jsondata['data']['country'],
                'region':jsondata['data']['region'],
                'city':jsondata['data']['city'],
                'county':jsondata['data']['county'],
                'isp':jsondata['data']['isp'],
                'ip':jsondata['data']['ip']}

    def get_ip_by_host(self,host):
        """ 获取远程主机的ip地址

        :param str host: 远程主机
        :return: ip地址
        :rtype: str
        """
        return socket.gethostbyname(host)

    @property
    def local_ip(self):
        ipinfo = request.urlopen('http://www.whereismyip.com').read()
        local_ip = re.search('\d+\.\d+\.\d+\.\d+',ipinfo.decode('utf-8')).group()
        return local_ip

    @property
    def host_name(self):
        return socket.gethostname()

    @property
    def inner_ip(self):
        return socket.gethostbyname(self.host_name)



if __name__ == '__main__':
    ipt = IPTools()
    print(ipt.local_ip)
    print(ipt.ip_belong('1.193.162.91'))
    print(ipt.host_name)
    print(ipt.inner_ip)

    print(ipt.get_ip_by_host('sports.sina.com.cn'))
    '''
    url = "http://ip.taobao.com/service/getIpInfo.php?ip=14.154.187.32"
    jsondata = json.loads(request.urlopen(url).read().decode('utf-8'))
    print(jsondata['data'])

    print(ipt.ip_belong('50.240.46.244'))'''