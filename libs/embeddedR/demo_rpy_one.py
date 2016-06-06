# coding=UTF-8

import rpy2.robjects as robjects
from rpy2.robjects import FloatVector
from rpy2.robjects.packages import importr
stats = importr('stats')
base = importr('base')
from libs.file.class_statadata import Statadata

stata_file = r'D:\data\test\wage1.dta'
stdata = Statadata(stata_file)
mdata = stdata.read()
rdata = mdata[['lwage','educ','exper','tenure']]

lwage = FloatVector(mdata['lwage'])
educ = FloatVector(mdata['educ'])
exper = FloatVector(mdata['exper'])
tenure = FloatVector(mdata['tenure'])

robjects.globalenv["lwage"] = lwage
robjects.globalenv["educ"] = educ
robjects.globalenv["exper"] = exper
robjects.globalenv["tenure"] = tenure

lm_obj = stats.lm("lwage ~ educ + exper + tenure")
print(list(lm_obj))
sm_obj = base.summary(lm_obj)
print(list(sm_obj))

print('---------------')
robjects.r("lmobj <- lm('lwage ~ educ+exper+tenure')")
robjects.r("x <- c(age=1,female=2)")
print(list(robjects.r('x["age"]')))
result = list(robjects.r('lmobj["coefficients"]'))
print(type(result))
for item in result[0]:
    print(item)
'''
ctl = FloatVector([4.17,5.58,5.18,6.11,4.50,4.61,5.17,4.53,5.33,5.14])
trt = FloatVector([4.81,4.17,4.41,3.59,5.87,3.83,6.03,4.89,4.32,4.69])
group = base.gl(2, 10, 20, labels = ["Ctl","Trt"])
weight = ctl + trt

robjects.globalenv["weight"] = weight
robjects.globalenv["group"] = group
lm_D9 = stats.lm("weight ~ group")
print(type(lm_D9))
print('hello',list(lm_D9.rx(1)))

# omitting the intercept
lm_D90 = stats.lm("weight ~ group - 1")
print('new',type(base.summary(lm_D90)))

sv = robjects.StrVector('ababbc')
fac = robjects.FactorVector(sv)
print(list(fac))

stats = importr('stats')
rnorm = stats.rnorm
print(list(rnorm(100)))
formals = rnorm.formals()
print(list(formals.names))'''