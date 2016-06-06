# coding=UTF-8

# -----------------------------------------------
# class_chart文件
# @class: Chart类
# @introduction: Chart类是作图的超类
# @dependency: pandas,matplotlib
# @author: plutoese
# @date: 2016.05.19
# ------------------------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
from pylab import *

# 支持汉字字符集
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


class Chart:
    """ Chart类是作图的通用接口

    :param str style: 格式名
    """
    def __init__(self, style='ggplot'):
        # 设置样式
        plt.style.use(style)

    def plot(self,df=None,type=None,**parameter):
        if type == 'bar':
            df.plot.bar(**parameter)
        if type == 'barh':
            df.plot.barh(**parameter)
        if type == 'hist':
            df.hist(**parameter)
        if type == 'scatter':
            df.plot.scatter(**parameter)
        if type == 'scatter matrix':
            scatter_matrix(df,diagonal='kde',**parameter)

    def add_title(self,title):
        """ 添加标题

        :param str title: 标题
        :return: 无返回值
        """
        plt.title(title)

    def add_xlabel(self,xlabel,*args, **kwargs):
        """ 添加x轴说明

        :param str xlabel: x轴说明
        :param args:
        :param kwargs:
        :return: 无返回值
        """
        plt.xlabel(xlabel)

    def add_ylabel(self,ylabel,*args, **kwargs):
        """ 添加y轴说明

        :param str ylabel: x轴说明
        :param args:
        :param kwargs:
        :return:
        """
        plt.ylabel(ylabel)

    def show(self):
        """ 显示图形

        :return: 无返回值
        """
        plt.show()

    def save(self,filename=None):
        """ 储存图形

        :param str filename: 图形文件名
        :return: 无返回值
        """
        plt.savefig(filename)


if __name__ == '__main__':
    df = pd.DataFrame(np.random.randn(1000, 4), columns=['a', 'b', 'c', 'd'])
    df2 = pd.DataFrame(np.random.rand(10, 4), columns=['a', 'b', 'c', 'd'])
    df4 = pd.DataFrame({'a': np.random.randn(1000) + 1, 'b': np.random.randn(1000),
                        'c': np.random.randn(1000) - 1}, columns=['a', 'b', 'c'])
    mcahrt = Chart()
    mcahrt.plot(df2,type='scatter',x='a', y='b', s=df['c']*200)
    mcahrt.add_title('我们特别好')
    mcahrt.add_xlabel('怎么补')
    mcahrt.show()

