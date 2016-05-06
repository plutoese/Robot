# coding=UTF-8

import re
import json

'''
fp = open('E:\\gitrobot\\files\\publication\\ssci_urban studies_raw.txt','rb')

ssci_economics = []
journal = []
for d in fp.readlines():
    item = d.decode()
    if re.match('^\d',item) is not None:
        name = re.split('\r\n',re.split('\.\s',item)[1])[0]
        if len(journal) < 1:
            journal.append(name)
        else:
            print('JOURANL PROBLEM!!!!!!')

    if re.search('ISSN:',item) is not None:
        issn = re.split('\r\n',re.split(':\s',item)[1])[0]
        if len(journal) == 1:
            journal.append(issn)
        else:
            print('ISSN PROBLEM!!!!!!')

    if len(journal) == 2:
        ssci_economics.append(journal)
        journal = []

print(ssci_economics)
print(len(ssci_economics))
#out_file = r'E:\gitrobot\files\publication\ssci_urban studies_json.txt'
#json.dump(ssci_economics, fp=open(out_file,'w'))

'''
papers = json.load(open(r'E:\gitrobot\files\publication\ssci_economics_json.txt'))
print(papers)
print(len(papers))