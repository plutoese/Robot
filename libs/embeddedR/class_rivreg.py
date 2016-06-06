# coding=UTF-8

# -----------------------------------------------
# class_rivreg文件
# @class: Rivreg类
# @introduction: Rivreg类用来进行工具变量法
# @dependency: rpy2
# @author: plutoese
# @date: 2016.05.20
# ------------------------------------------------

import numpy as np
import pandas as pd
import rpy2.robjects as robjects
from libs.embeddedR.class_rthread import RThread
from rpy2.robjects.packages import importr
from rpy2.robjects import FloatVector, IntVector, StrVector, Matrix, DataFrame, Vector
from libs.file.class_statadata import Statadata


class Rivreg:
    """ Rivreg类用来进行工具变量法

    """
    def __init__(self,robj=None,yvar=None,xvar=None,zvar=None):
        self.robj = robj
        self.lm_str = ''.join(['lm("',yvar,' ~ ',' + '.join(xvar),' | ',' + '.join(zvar),'")'])
        self.robj.R.r(''.join(['lm_obj <- ',self.lm_str]))
        self.robj.R.r('slm_obj <- summary(lm_obj)')

    def __repr__(self):
        str_line = ''.join(['-']*60)
        str_nobs = 'Number of Obs: {}'.format(self.nobs)
        str_rsquared = 'Rsqaured: {0:.4f}, Adj.Rsquared: {1:.4f}'.format(self.Rsquared[0],self.adj_Rsquared[0])
        str_f = 'F({0},{1}): {2:.2f}'.format(int(self.fstatistic[1]),int(self.fstatistic[2]),self.fstatistic[0])
        return ''.join([str_line,'\n',
                        self.model,'\n',
                        str_nobs,'\n',
                        str_rsquared,'\n',
                        str_f,'\n',
                        '\n',
                        self.coefficients.__repr__(),
                        '\n',str_line])

    @property
    def nobs(self):
        return self.data.shape[0]

    @property
    def model(self):
        """ 返回回归模型

        :return:
        """
        return self.lm_str

    @property
    def coefficients(self):
        return self.robj.get_var('slm_obj$coefficients')

    @property
    def data(self):
        return self.robj.get_var('lm_obj$model')

    @property
    def residuals(self):
        return self.robj.get_var('slm_obj$residuals')

    @property
    def fitted(self):
        return self.robj.get_var('lm_obj$fitted.values')

    @property
    def fstatistic(self):
        return self.robj.get_var('slm_obj$fstatistic')

    @property
    def sigma(self):
        return self.robj.get_var('slm_obj$sigma')

    @property
    def rank(self):
        return self.robj.get_var('lm_obj$rank')

    @property
    def df(self):
        return self.robj.get_var('slm_obj$df')

    @property
    def Rsquared(self):
        return self.robj.get_var('slm_obj$r.squared')

    @property
    def adj_Rsquared(self):
        return self.robj.get_var('slm_obj$adj.r.squared')

    @property
    def cov(self):
        return self.robj.get_var('slm_obj$cov.unscaled')

    @property
    def qr(self):
        return self.robj.get_var('lm_obj$qr$qr')

if __name__ == '__main__':
    rthread = RThread()

    stata_file = r'D:\data\test\MROZ.dta'
    stdata = Statadata(stata_file)
    mdata = stdata.read()
    rdata = mdata[['lwage','educ','fatheduc']]
    rthread.create_vars(rdata)

    lm = Rivreg(robj=rthread,xvar=['educ'],yvar='lwage',zvar=['fatheduc'])
    '''
    print(lm.coefficients)
    print(lm.fstatistic)
    print(lm.sigma)
    print(lm.df)
    print(lm.qr)
    print(lm.Rsquared)
    print(lm.adj_Rsquared)
    print(lm.cov)
    print(lm.rank)
    '''
    #print(lm.data)
    #print(lm.nobs)
    '''
    base = importr('base')
    d = {'a':IntVector((1,2,3)),'b':base.I(StrVector('abc'))}
    mvar = DataFrame(d)
    rthread.create_vars({'var':mvar})
    print(rthread.get_var('var'))'''
    #print(lm)
