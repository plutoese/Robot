# coding=UTF-8

import pickle
import re
from collections import OrderedDict

F = open(r'E:\gitrobot\files\literature\literature_list.pkl', 'rb')
literature_list = pickle.load(F)

literature = OrderedDict()

for llist in literature_list:
    content = str(llist.find_all('p'))
    content = re.split('</p>\]',re.split('\[<p>',content)[1])[0]
    items = re.split('\n',content)

    one_literature = dict()
    for item in items:
        if '{Title}' in item:
            title = re.sub('\s+','',re.split('}: ',item)[1])
        if '{Author}' in item:
            one_literature['author'] = [re.sub('\s+','',author) for author in re.split('\{Author\}\: ',item)
                                        if len(author) > 0]
        if '{Author Address}' in item:
            one_literature['address'] = [re.sub('\s+','',address) for address in re.split(';',re.split('\}\: ',item)[1])
                                        if len(address) > 0]
        if '{Journal}' in item:
            one_literature['journal'] = re.sub('\s+','',re.split('\}\: ',item)[1])
        if '{Year}' in item:
            one_literature['year'] = re.sub('\s+','',re.split('\}\: ',item)[1])
        if '{Issue}' in item:
            one_literature['issure'] = re.sub('\s+','',re.split('\}\: ',item)[1])
        if '{Pages}' in item:
            one_literature['pages'] = re.sub('\s+','',re.split('\}\: ',item)[1])
        if '{Keywords}' in item:
            one_literature['keyword'] = [re.sub('\s+','',keyword) for keyword in re.split(';',re.split('\}\: ',item)[1])
                                         if len(keyword) > 0]
        if '{Abstract}' in item:
            one_literature['abstract'] = re.split('\}\: ',item)[1]
        if '{ISBN/ISSN}' in item:
            one_literature['ISBN/ISSN'] = re.sub('\s+','',re.split('\}\: ',item)[1])
        if '{Database Provider}' in item:
            literature[title] = one_literature
            one_literature = dict()

for title in literature:
    print(title)
    print(literature[title])
    print('*************************************')

print(len(literature))



