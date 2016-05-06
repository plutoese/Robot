# coding=UTF-8

# --------------------------------------------------------------
# class_individual文件
# @class: Individual类
# @introduction: Individual类代表个体
# @dependency:
# @author: plutoese
# @date: 2016.05.03
# --------------------------------------------------------------

import re


class Individual:
    """Individual类代表个体

    :param str name: 个体的姓名
    :param str type: 个体的类型
    :param list preference: 个体的偏好
    :return: 无返回值
    """
    def __init__(self,name,type=None,preference=None):
        # 设置姓名
        self.name = name
        # 设置类型
        if type is None:
            self.type = re.match('^[a-zA-Z]+',name).group()
        else:
            self.type = type

        # 设置偏好
        self.preference_list = preference
        # 设置偏好字典，即偏好序
        if preference is None:
            self.preference = None
        else:
            self.preference = dict(zip(preference,range(1,len(preference)+1)))
        # 设置状态
        # 状态变量：是否可以进行匹配（或订婚），如果已经订婚，则为True，否则为False。
        self.available = True
        # 状态变量：匹配对象（订婚对象）
        self.engageTo = None

    def set_preference(self,preference):
        """ 设置个体偏好

        :param list preference: 个体的偏好
        :return: 无返回值
        """
        self.preference_list = preference
        self.preference = dict(zip(preference,range(1,len(preference)+1)))

    def propose_to(self,individual):
        """追求对象individual

        :param Indicidual individual: 被追求对象
        :return: 无返回值
        """
        # 弹出心仪对象
        if len(self.preference_list) > 0:
            self.preference_list.pop(0)

        if individual.be_proposed_by(self):
            self.available = False
            self.engageTo = individual

    def be_proposed_by(self,individual):
        if self.available:
            self.available = False
            self.engageTo = individual
            return True
        else:
            new_engageTo,who = self.prefer(self.engageTo,individual)
            if who > 1:
                self.engageTo.available = True
                self.engageTo.engageTo = None
                self.engageTo = new_engageTo
                return True
            else:
                return False

    def prefer(self,one,theother):
        if self.preference.get(one.name) <= self.preference.get(theother.name):
            return one,1
        return theother,2

    def __repr__(self):
        if self.engageTo is None:
            engage_to = 'None'
        else:
            engage_to = self.engageTo.name
        first_line = ''.join([(''.join(['-']*20)),'\n'])
        name = ''.join(['name: ',self.name,'\n'])
        status = ''.join(['avaiable: ',str(self.available),'\n',
                          'engageTo: ',engage_to,'\n'])
        last_line = ''.join([(''.join(['-']*20)),'\n'])
        return ''.join([first_line,name,status,last_line])

if __name__ == '__main__':
    m1 = Individual(name='m1',preference=['w1','w2'])
    m2 = Individual(name='m2',preference=['w2','w1'])
    w1 = Individual(name='w1',preference=['m1','w2'])
    w2 = Individual(name='w2',preference=['m1'])
    print(m1.type)
    w2.propose_to(m1)
    print('********* Round One ***********')
    print(w2)
    print(m1)
    w1.propose_to(m1)
    print('********* Round Two ***********')
    print(w1)
    print(w2)
    print(m1)

