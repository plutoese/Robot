from bokeh.charts import Scatter, output_file, show
from bokeh.sampledata.iris import flowers as data
import pandas as pd
import numpy as np

scatter = Scatter(data,x='petal_length',y='petal_width',color='species',legend=True)
#output_file('iris_sample.html')
#show(scatter)

df = pd.DataFrame({'value':np.random.randint(0,100,20)})

df['group'] = pd.cut(df.value,3,labels=['low','median','high'])
print(df)