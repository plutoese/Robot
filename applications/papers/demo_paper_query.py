# coding=UTF-8

from libs.database.class_mongodb import MongoDB
from libs.file.class_Excel import Excel

mongo = MongoDB()
mongo.connect('paper','literature')

result = mongo.collection.find({}).distinct('journal')
print(result)
''''
result = mongo.collection.find({'journal':'Journal of Econometrics',
                                'keyword':{'$exists':True}})

keyword = set()
for item in result:
    keyword.update([item.lower() for item in item['keyword']])

mdata = [[item] for item in sorted(keyword)]

outfile = r'd:\down\keywords.xlsx'
moutexcel = Excel(outfile)
moutexcel.new().append(mdata, 'mysheet')
moutexcel.close()'''

result = mongo.collection.find({'keyword':'ARMA'})
result = mongo.collection.find({'keyword':{'$regex':'^(a|A)utocorrelation$'}})
for item in result:
    print(item['keyword'])