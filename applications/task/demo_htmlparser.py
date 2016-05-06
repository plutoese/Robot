# coding=UTF-8

from bs4 import BeautifulSoup

File = 'E:\\temp\\book\\Introductory_Econometrics.html'
fdata = open(File,'r',encoding='UTF-8').read()
bsobject = BeautifulSoup(fdata,'lxml')
print(bsobject.title)
