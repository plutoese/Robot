# coding=UTF-8

import numpy as np
import statsmodels.api as sm

spector_data = sm.datasets.spector.load()
spector_data.exog = sm.add_constant(spector_data.exog, prepend=True)

mod = sm.OLS(spector_data.endog, spector_data.exog)
res = mod.fit()
res_sum = res.summary()
print(dir(res))
print(dir(res_sum))


'''
a = np.arange(5)
print(a)
print(a.dtype)

m = np.array([np.arange(4),np.arange(4)])
print(m)

A = np.mat('0 1 2; 1 0 3; 4 -3 8')
print(A)
invA = np.linalg.inv(A)
print(invA)
print(A*invA)'''




