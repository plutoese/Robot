# coding=UTF-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print(plt.style.available)
plt.style.use('ggplot')

ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))

ts = ts.cumsum()
df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))
df = df.cumsum()
print(df)
df.hist()
plt.show()