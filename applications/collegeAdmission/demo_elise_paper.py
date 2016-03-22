# coding=UTF-8

import re
from libs.file.class_Excel import Excel
from libs.database.class_mongodb import MongoDB
import pandas as pd
from bokeh.charts import Scatter, output_file, show
from bokeh.sampledata.iris import flowers as data


class ElisePaper:
    def __init__(self):
        self.mongo = MongoDB()
        province_economy = Excel('E:\\data\\college\\province.xlsx').read()
        self.province_economy_dict = dict([(str(int(item[0])),item[2]) for item in province_economy[1:]])
        self.mongo.connect('region','province')
        self.province_dict = dict([(item['acode'],item['region']) for item in self.mongo.collection.find({})])

    def get_data_by_region(self,acode,subject='理科'):
        mresult = [['学校','类型','录取平均分','学校地区','学校评分','地区收入']]
        self.mongo.connect('college','entranceexam')
        query_result = self.mongo.collection.find({'student_region':acode,'subject':subject})
        self.mongo.connect('college','collegeinfo')
        for item in query_result:
            rating = self.mongo.collection.find_one({'name':item['university']})['rating']
            income = self.province_economy_dict[item['university_region']]
            mresult.append([item['university'],item['type'],item['average_score'],item['university_region'],
                            rating,income])
        return mresult

    def get_college_data(self):
        self.mongo.connect('college','entranceexam')
        colleges = self.mongo.collection.find({}).distinct('university')
        self.mongo.connect('college','collegeinfo')
        records = self.mongo.collection.find({'name':{'$in':colleges}},
                                             projection={'_id':0,'name':1,'rating':1,'score':1,'region':1,'project':1,'type':1})

        result = [record for record in records if len(record['region']) < 2]
        result = dict([(item['rating'],item) for item in result])
        mresult = [['排名','学校','类型','评分','地区','地区可支配收入']]
        for item in sorted(result):
            region = result[item]['region'][0]
            region_income = self.province_economy_dict[region]
            mresult.append([result[item]['rating'],result[item]['name'],
                            result[item]['type'],result[item]['score'],
                            region,region_income])
        return mresult


    def close(self):
        self.mongo.close()

if __name__ == '__main__':
    elise = ElisePaper()
    acode = '420000'
    mdata1 = elise.get_data_by_region(acode)
    mdata2 = elise.get_college_data()
    print(mdata1)
    d1 = {'录取平均分':[item[2] for item in mdata1[1:]],
          '学校':[item[0] for item in mdata1[1:]],
          '学校排名':[item[4] for item in mdata1[1:]],
          '学校地区':[item[3] for item in mdata1[1:]],
          '类型':[item[1] for item in mdata1[1:]],
          '地区可支配收入':[item[5] for item in mdata1[1:]]}
    pd1 = pd.DataFrame(d1)
    pd1['地区状态'] = pd.cut(pd1['地区可支配收入'],3,labels=['低收入','中等收入','高收入'])
    #pd1['地区状态'] = pd.cut(pd1['地区可支配收入'],5,labels=['低收入','较低收入','中等收入','较高收入','高收入'])
    pd1['地区'] = '非本地'
    pd1['地区'][pd1['学校地区'].eq(acode)] = '本地'
    pd1 = pd1[pd1['录取平均分']>500]
    pd1 = pd1[pd1['类型'].eq('综合')]
    print(pd1)
    pd1 = pd1[pd1['学校地区'].ne(acode)]
    pd1.to_csv('d:\\down\\result1.csv')
    '''
    print(mdata2)
    d2 = {'rating':[item[0] for item in mdata2[1:]],
          '学校评分':[item[3] for item in mdata2[1:]],
          '地区可支配收入':[item[5] for item in mdata2[1:]]}
    pd2 = pd.DataFrame(d2)
    print(pd2)

    scatter = Scatter(pd2,x='地区可支配收入',y='学校评分',title='地区收入与学校质量')
    output_file('iris_sample.html')
    show(scatter)'''

    scatter = Scatter(pd1,x='录取平均分',y='学校排名',color='地区状态',
                      marker='地区状态',title='录取平均分与学校排名',legend=True)
    output_file('result1.html')
    show(scatter)

    elise.close()


