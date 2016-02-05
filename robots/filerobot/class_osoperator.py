# coding=UTF-8

# --------------------------------------------------------------
# class_osoperator文件
# @class: OSOperator
# @introduction: OSOperator类进行基本的文件操作
# @dependency: File, Path类及shutil模块
# @author: plutoese
# @date: 2016.02.05
# --------------------------------------------------------------

import os
import shutil
from libs.file.class_Excel import Excel


class OSOperator:
    """OSOperator类进行基本的文件操作

    """
    def __init__(self):
        pass

    @classmethod
    def read_from_dir(cls,path,outexcel=False,outpath=None):
        files = os.listdir(path)
        if outexcel:
            moutexcel = Excel(outpath)
            moutexcel.new().append([[item,item] for item in files],'sheet1')
            moutexcel.close()
        else:
            return files

    @classmethod
    def move_to(cls,source,destination):
        shutil.move(source, destination)

    @classmethod
    def copy_to(cls,source,destination):
        shutil.copy(source,destination)

    @classmethod
    def delete(cls,path):
        os.unlink(path)

    @classmethod
    def rmdir(cls,path):
        os.rmdir(path)

if __name__ == '__main__':
    op = OSOperator()
    op.read_from_dir(r'E:\piles\teacher\Applied statistics',True,'d:\\down\\result.xlsx')




