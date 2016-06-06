# coding=UTF-8

# -----------------------------------------------
# class_rthread文件
# @class: RThread类
# @introduction: RThread类用来初始化R环境
# @dependency: rpy2
# @author: plutoese
# @date: 2016.05.20
# ------------------------------------------------

import numpy as np
import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.rinterface import RNULLType
from rpy2.robjects import FloatVector, IntVector, StrVector, Matrix, DataFrame, Vector
from libs.file.class_statadata import Statadata


class RThread:
    """ RThread类用来初始化R环境

    :var robjects R: R对象
    """
    def __init__(self):
        self.R = robjects

    def create_vars(self,vars=None):
        """ 在R中创建变量

        :param dict,pd.Dataframe vars: 变量数据
        :return: 无返回值
        """
        if isinstance(vars,dict):
            var_names = vars.keys()
        elif isinstance(vars,pd.DataFrame):
            var_names = list(vars.columns)
        else:
            print('vars is not dict or dataframe!')
            var_names = []

        for var_name in var_names:
            if isinstance(vars[var_name],(list,pd.Series)):
                if isinstance(vars[var_name][0],(int,np.int8)):
                    self.R.globalenv[var_name] = IntVector(vars[var_name])
                if isinstance(vars[var_name][0],(float,np.float32)):
                    self.R.globalenv[var_name] = FloatVector(vars[var_name])
            else:
                self.R.globalenv[var_name] = vars[var_name]

    def get_var(self,varname):
        """ 返回R中的一个变量

        :param str varname: 变量名
        :return: 无返回值
        """
        # 获得变量的值

        value, type, indexs = self._r_variable(varname)

        if type == 'vector':
            return pd.Series(list(value),index=indexs[0])
        if type == 'matrix':
            return pd.DataFrame(np.matrix(value),index=indexs[0],columns=indexs[1])
        if type == 'dataframe':
            dframe = pd.DataFrame(pd.Series(list(item)) for item in value)
            dframe = dframe.T
            dframe.index = indexs[0]
            dframe.columns = indexs[1]
            return dframe

    def _r_variable(self,variable_name=None):
        """ 辅助函数，提取variable的信息

        :param variable_name:
        :return:
        """
        value = self.R.r(variable_name)
        if isinstance(value,(IntVector,FloatVector)):
            type = 'vector'
            name = self.R.r(''.join(['names(',variable_name,')']))
            if isinstance(name,RNULLType):
                name = None
            else:
                name = list(name)
            return value,type,(name,)

        if isinstance(value,Matrix):
            type = 'matrix'
        if isinstance(value,DataFrame):
            type = 'dataframe'
        colnames = self.R.r(''.join(['colnames(',variable_name,')']))
        rownames = self.R.r(''.join(['rownames(',variable_name,')']))
        if isinstance(colnames,RNULLType):
            colnames = None
        else:
            colnames = list(colnames)
        if isinstance(rownames,RNULLType):
            rownames = None
        else:
            rownames = list(rownames)
        return value,type,(rownames,colnames)


class Rreg:
    """ 调用lm函数进行回归分析

    """
    def __init__(self,robj=None,yvar=None,xvar=None):
        self.robj = robj
        self.lm_str = ''.join(['lm("',yvar,' ~ ',' + '.join(xvar),'")'])
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

    stata_file = r'D:\data\test\wage1.dta'
    stdata = Statadata(stata_file)
    mdata = stdata.read()
    rdata = mdata[['lwage','educ','exper','tenure']]
    rthread.create_vars(rdata)

    lm = Rreg(robj=rthread,xvar=['educ','exper','tenure'],yvar='lwage')
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
    print(lm)
