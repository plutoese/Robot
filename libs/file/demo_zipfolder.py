# coding=UTF-8

import os
import re
from libs.file.class_pathparse import PathParse
from libs.file.class_path import Path
import zipfile
import shutil

file_path = Path('E:\\piles\\teacher','E:\\piles\\teacher')
zip_file_name = ''.join([file_path.parse.file_name_with_dir,'.zip'])
print(zip_file_name)
'''
newZip = zipfile.ZipFile(zip_file_name, 'w')
print('----------------------------------------------------')
for item in os.walk(file_path.parse.file_name_with_dir):
    print(item)
    relative_path = os.path.relpath(item[0],'E:\\piles\\teacher')
    for file in item[2]:
        newZip.write(''.join([item[0],'\\',file]), compress_type=zipfile.ZIP_DEFLATED)

newZip.close()'''

shutil.make_archive(zip_file_name,'zip','E:\\piles\\teacher','.')






