# coding=UTF-8

from ggplot import *
from pymongo import *

#ggplot(mtcars, aes('wt', 'mpg')) + geom_point()
client =MongoClient('mongodb://plutoese:z1Yh29@139.196.189.191:3717')
db = client['test']
test = db['test']
print(test.find())
print(client.database_names())


