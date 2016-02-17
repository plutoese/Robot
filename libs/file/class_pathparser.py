# coding=UTF-8

# --------------------------------------------------------------
# class_pathparser文件
# @class: PathParser
# @introduction: PathParser类用来解析目录或者文件名称
# @dependency: os, os.path包
# @author: plutoese
# @date: 2016.01.28
# --------------------------------------------------------------

import os
import re
import datetime


class PathParser:
    # 属性表
    # 特殊字符
    __special_character = '@#%$&{='
    # 特殊字符，除了压缩字符
    __special_character_without_zip = '@#%$&{'
    # 压缩特殊字符
    __zip_character = '='
    # 绝对路径文件夹或文件名
    __path_name_with_absolute_path = None
    # 路径名
    __directory = None
    # 完整文件名
    __path_name = None
    # 没有后缀的文件名
    __path_name_without_extension = None
    # 后缀
    __path_extension = None
    # 没有特殊字符的路径名称
    __path_name_without_special_characters = None
    # 没有特殊字符的绝对路径名称
    __path_name_with_absolute_path_without_special_characters = None
    # 路径名中特殊字符部分
    __special_character_part = None

    """File类用来处理文件和文件夹解析

    """
    def __init__(self, path_name_with_absolute_path):
        if os.path.isfile(path_name_with_absolute_path) or os.path.isdir(path_name_with_absolute_path):
            self.__path_name_with_absolute_path = path_name_with_absolute_path
        else:
            print('{} is not a directory!'.format(path_name_with_absolute_path))
            raise FileNotFoundError

        self.__directory, self.__path_name = os.path.split(self.__path_name_with_absolute_path)
        if os.path.isdir(self.__path_name_with_absolute_path):
            self.__directory = self.__path_name_with_absolute_path

        tmp_split = re.split('\.',self.__path_name)
        if len(tmp_split) < 2:
            self.__path_name_without_extension = tmp_split[0]
        elif len(tmp_split) < 3:
            self.__path_name_without_extension, self.__path_extension = tmp_split
        else:
            self.__path_extension = tmp_split.pop(len(tmp_split)-1)
            self.__path_name_without_extension = '.'.join(tmp_split)
        # 解析路径名
        self.__path_name_parse()

    @property
    def last_modified(self):
        return datetime.datetime.fromtimestamp(os.path.getmtime(self.__path_name_with_absolute_path))

    @property
    def path_name_with_absolute_path(self):
        return self.__path_name_with_absolute_path

    @property
    def directory(self):
        return self.__directory

    @property
    def path_name_without_extension(self):
        return self.__path_name_without_extension

    @property
    def path_name(self):
        return self.__path_name

    @property
    def path_name_without_special_characters(self):
        return self.__path_name_without_special_characters

    @property
    def path_name_with_absolute_path_without_special_characters(self):
        return self.__path_name_with_absolute_path_without_special_characters

    @property
    def extension(self):
        return self.__path_extension

    @property
    def special_character_part(self):
        return self.__special_character_part

    @property
    def author(self):
        return self.__author

    @property
    def time(self):
        if self.__time is not None:
            if len(self.__time) > 2:
                return datetime.datetime(*self.__time)
            elif len(self.__time) > 1:
                return datetime.datetime(*self.__time,day=1)
            else:
                return datetime.datetime(*self.__time,month=1,day=1)
        else:
            return None

    @property
    def version(self):
        return self.__version

    @property
    def tags(self):
        return self.__tags

    @property
    def dirs(self):
        return self.__dirs

    @property
    def projects(self):
        return self.__projects

    @property
    def is_packed(self):
        return self.__packed

    @property
    def is_having_special_character(self):
        if self.__special_character_part is None:
            return False
        else:
            return True

    def __repr__(self):
        if self.time is None:
            time = ['None']
        else:
            time = self.time

        if self.tags is None:
            tags = ['None']
        else:
            tags = self.tags

        if self.projects is None:
            projects = ['None']
        else:
            projects = self.projects

        fmt = ''.join(['absolute path name                  : {0}\n',
                       'path directory                      : {1}\n',
                       'path name                           : {2}\n',
                       'path name without extension         : {3}\n',
                       'path name without special characters: {4}\n',
                       'special character part              : {5}\n'
                       'last modified                       : {6}\n',
                       '@author                             : {7}\n',
                       '@time                               : {8}\n',
                       '@version                            : {9}\n',
                       '@dirs                               : {10}\n',
                       '@tags                               : {11}\n',
                       '@projects                           : {12}\n',
                       '@is packed                          : {13}\n'])
        return fmt.format(self.path_name_with_absolute_path,
                          self.directory,
                          self.path_name,
                          self.path_name_without_extension,
                          self.path_name_without_special_characters,
                          self.special_character_part,
                          self.last_modified,
                          self.author,
                          self.time,
                          self.version,
                          self.dirs,
                          ', '.join(tags),
                          ', '.join(projects),
                          self.is_packed)

    def __path_name_parse(self):
        """辅助函数，分解文件名：作者，时间，版本，标签，目录，项目名称

        :return: 无返回值
        """
        self.__author = None
        self.__time = None
        self.__version = None
        self.__tags = None
        self.__dirs = None
        self.__projects = None
        self.__packed = False

        # 没有特殊字符的文件名称
        if self.extension is not None:
            self.__path_name_without_special_characters = ''.join([re.split('[@{#$%&=]',self.path_name_without_extension)[0],'.',
                                                          self.__path_extension])
        else:
            self.__path_name_without_special_characters = re.split('[@{#$%&=]',self.path_name_without_extension)[0]
        self.__path_name_with_absolute_path_without_special_characters = os.path.join(self.directory,
                                                                                      self.path_name_without_special_characters)
        self.__special_character_part = re.split(re.split('\.',self.__path_name_without_special_characters)[0],
                                                 self.path_name_without_extension)[1]
        if re.match('^$',self.__special_character_part) is not None:
            self.__special_character_part = None

        # 析出作者
        tmp_search_result = re.search('@[^{#$%&=]+',self.__path_name_without_extension)
        if tmp_search_result is not None:
            self.__author = re.sub('@','',tmp_search_result.group())

        # 析出时间
        tmp_search_result = re.search('#[^@{$%&=]+',self.__path_name_without_extension)
        if tmp_search_result is not None:
            self.__time = [int(item) for item in re.split('#',tmp_search_result.group()) if len(item) > 0]

        # 析出版本号
        tmp_search_result = re.search('$[^@#{%&=]+',self.__path_name_without_extension)
        if tmp_search_result is not None:
            self.__version = re.sub('$','',tmp_search_result.group())

        # 析出标签
        tmp_search_result = re.search('%[^@#${&=]+',self.__path_name_without_extension)
        if tmp_search_result is not None:
            self.__tags = [item for item in re.split('%',tmp_search_result.group()) if len(item) > 0]

        # 析出目录
        tmp_search_result = re.search('&[^@#$%{=]+',self.__path_name_without_extension)
        if tmp_search_result is not None:
            self.__dirs = [item for item in re.split('&',tmp_search_result.group()) if len(item) > 0]

        # 析出项目名
        tmp_search_result = re.search('\{[^@#$%&=]+',self.__path_name_without_extension)
        if tmp_search_result is not None:
            self.__projects = [item for item in re.split('\{',tmp_search_result.group()) if len(item) > 0]

        # 是否打包
        tmp_search_result = re.search(self.__zip_character,self.__path_name_without_extension)
        if tmp_search_result is not None:
            self.__packed = True


if __name__ == '__main__':
    mpath = PathParser('D:\\down\\demo@glen#2012%database%mongodb%test   blank{自科基金{社科基金&geeker.xlsx')
    #mpath = PathParser(r'E:\room\libs\creator')
    print(mpath)
    print(mpath.path_name_with_absolute_path_without_special_characters)
    print(mpath.is_having_special_character)
