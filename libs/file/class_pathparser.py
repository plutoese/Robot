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
    """ File类用来处理文件和文件夹解析

    """
    def __init__(self, path_name_with_absolute_path):
        # 设定类对象的变量
        # 特殊字符
        self.__special_character = '@#%$&{='
        # 特殊字符，除了压缩字符
        self.__special_character_without_zip = '@#%$&{'
        # 压缩特殊字符
        self.__zip_character = '='
        # 绝对路径文件夹或文件名
        self.__path_name_with_absolute_path = None
        # 路径名
        self.__directory = None
        # 完整文件名
        self.__path_name = None
        # 没有后缀的文件名
        self.__path_name_without_extension = None
        # 后缀
        self.__path_extension = None
        # 没有特殊字符的路径名称
        self.__path_name_without_special_characters = None
        # 没有特殊字符的绝对路径名称
        self.__path_name_with_absolute_path_without_special_characters = None
        # 路径名中特殊字符部分
        self.__special_character_part = None

        # 如果path_name_with_absolute_path不是路径名或者文件名，那么返回错误提示
        if os.path.isfile(path_name_with_absolute_path) or os.path.isdir(path_name_with_absolute_path):
            self.__path_name_with_absolute_path = path_name_with_absolute_path
        else:
            print('{} is not a directory!'.format(path_name_with_absolute_path))
            raise FileNotFoundError

        # 拆分路径和文件名
        self.__directory, self.__path_name = os.path.split(self.__path_name_with_absolute_path)
        # 如果解析的是路径名，那么路径就是绝对路径名本身
        if os.path.isdir(self.__path_name_with_absolute_path):
            self.__directory = self.__path_name_with_absolute_path

        # 解析文件名或者路径名
        tmp_split = re.split('\.',self.__path_name)
        # 若是路径名，那么self.__path_extension是None
        if len(tmp_split) < 2:
            self.__path_name_without_extension = tmp_split[0]
        # 若是文件名，那么拆分文件名和后缀
        elif len(tmp_split) < 3:
            self.__path_name_without_extension, self.__path_extension = tmp_split
        # 如果文件名中有“.”，遵守下面拆分规则
        else:
            self.__path_extension = tmp_split.pop(len(tmp_split)-1)
            self.__path_name_without_extension = '.'.join(tmp_split)
        # 解析路径名
        self.__path_name_parse()

    @property
    def last_modified(self):
        """ 返回最近更改时期

        :return: 返回最近更改时期
        :rtype: datetime.datetime对象
        """
        return datetime.datetime.fromtimestamp(os.path.getmtime(self.__path_name_with_absolute_path))

    @property
    def path_name_with_absolute_path(self):
        """ 返回绝对路径名或者全文件名

        :return: 返回绝对路径名或者全文件名
        :rtype: str
        """
        return self.__path_name_with_absolute_path

    @property
    def directory(self):
        """ 返回绝对路径名

        :return: 返回绝对路径名
        :rtype: str
        """
        return self.__directory

    @property
    def path_name_without_extension(self):
        """ 返回路径或者无后缀的文件名

        :return: 返回路径或者无后缀的文件名
        :rtype: str
        """
        return self.__path_name_without_extension

    @property
    def path_name(self):
        """ 路径名或者文件名

        :return: 路径名或者文件名
        :rtype: str
        """
        return self.__path_name

    @property
    def path_name_without_special_characters(self):
        """ 没有特殊字符的路径名或者文件名

        :return: 没有特殊字符的路径名或者文件名
        :rtype: str
        """
        return self.__path_name_without_special_characters

    @property
    def path_name_with_absolute_path_without_special_characters(self):
        """ 没有特殊字符的绝对路径名或者全文件名

        :return: 没有特殊字符的绝对路径名或者全文件名
        :rtype: str
        """
        return self.__path_name_with_absolute_path_without_special_characters

    @property
    def extension(self):
        """ 后缀

        :return: 后缀
        :rtype: str
        """
        return self.__path_extension

    @property
    def special_character_part(self):
        """ 路径名或者文件名中的特殊字符部分

        :return: 路径名或者文件名中的特殊字符部分
        :rtype: str
        """
        return self.__special_character_part

    @property
    def author(self):
        """ 作者

        :return: 作者
        :rtype: str
        """
        return self.__author

    @property
    def time(self):
        """ 时间

        :return: 时间
        :rtype: datetime.datetime对象
        """
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
        """ 版本

        :return: 版本
        :rtype: str
        """
        return self.__version

    @property
    def tags(self):
        """ 标签

        :return: 标签
        :rtype: list
        """
        return self.__tags

    @property
    def dirs(self):
        """ 路径

        :return: 路径
        :rtype: list
        """
        return self.__dirs

    @property
    def projects(self):
        """ 项目

        :return: 项目
        :rtype: list
        """
        return self.__projects

    @property
    def is_packed(self):
        """ 是否压缩

        :return: 是否压缩
        :rtype: bool
        """
        return self.__packed

    @property
    def is_having_special_character(self):
        """ 是否包含特殊字符

        :return: 是否包含特殊字符
        :rtype: bool
        """
        if self.__special_character_part is None:
            return False
        else:
            return True

    def __repr__(self):
        """ 类对象的str表达

        :return: 无返回值
        """
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

        # 析出没有特殊字符的路径名或者文件名
        if self.extension is not None:
            self.__path_name_without_special_characters = ''.join([re.split('[@{#$%&=]',self.path_name_without_extension)[0],'.',
                                                          self.__path_extension])
        else:
            self.__path_name_without_special_characters = re.split('[@{#$%&=]',self.path_name_without_extension)[0]

        # 析出没有特殊字符的绝对路径名或全文件名
        self.__path_name_with_absolute_path_without_special_characters = os.path.join(self.directory,
                                                                                      self.path_name_without_special_characters)
        # 析出路径名或文件名内的特殊字符部分
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
        tmp_search_result = re.search('\$[^@#{%&=]+',self.__path_name_without_extension)
        if tmp_search_result is not None:
            self.__version = re.sub('\$','',tmp_search_result.group())

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
    #mpath = PathParser(r'd:\down\选课手册导出@glen#2012%database%mongodb%test   blank{自科基金{社科基金&econometricsteaching=.zip')
    mpath = PathParser(r'E:\room\forawhile\python\Mining the Social Web#2014$2%python&python&book.pdf')
    #mpath = PathParser(r'E:\Room\forawhile\选课手册导出@glen#2012%database%mongodb%test   blank{自科基金{社科基金&econometricsteaching=')
    print(mpath)
    print(mpath.path_name_with_absolute_path_without_special_characters)
    print(mpath.is_having_special_character)
