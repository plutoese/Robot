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
    :return: 无返回值
    """
    def __init__(self,name):
        # 设置姓名
        self.name = name

        # 设置状态
        self.mate = None

    def set_preference(self,preference):
        """ 设置个体偏好

        :param list preference: 个体的偏好
        :return: 无返回值
        """
        self.preference_list = preference
        self.preference = dict(zip([item.name for item in preference],range(1,len(preference)+1)))

    def __repr__(self):
        if self.mate is None:
            mate = 'None'
        else:
            mate = self.mate.name
        first_line = ''.join([(''.join(['-']*20)),'\n'])
        name = ''.join(['name: ',self.name,'\n'])
        status = ''.join(['mate: ',mate,'\n',
                          'preference: ',','.join([item.name for item in self.preference_list]),'\n'])
        last_line = ''.join([(''.join(['-']*20)),'\n'])
        return ''.join([first_line,name,status,last_line])


class Proposer(Individual):
    """ 主动行动者（求婚者）

    :param str name: 个体的姓名
    :return: 无返回值
    """
    def __init__(self,name):
        Individual.__init__(self,name)

    def make_proposal_to(self,individual=None):
        """ 追求（求婚）某人

        :param Individual individual: 个人
        :return:
        """
        if individual is None:
            if self.more_proposal:
                individual = self.preference_list.pop(0)
            else:
                print('No one in your list!')
        if individual.name not in self.preference.keys():
            print(individual.name,'is not in your list!')

        if individual.be_proposed_by(self):
            self.mate = individual

    @property
    def more_proposal(self):
        """ 是否还要继续追求（求婚）

        :return: self.preference_list中是否还有元素
        :rtype: bool
        """
        if (len(self.preference_list) > 0) and (self.mate is None):
            return True
        else:
            return False


class Receiver(Individual):
    """ 被动接受者（被求婚者）

    :param str name: 个体的姓名
    :return: 无返回值
    """
    def __init__(self,name):
        Individual.__init__(self,name)

    def be_proposed_by(self,individual):
        """ 被individual对象追求（求婚）

        :param Individual individual: 求婚对象
        :return: 追求成功与否
        :rtype: bool
        """
        if self.mate is not None:
            # 如果有匹配对象，比较当前匹配对象和求婚对象，更偏好哪个
            perfer_mate, who = self.prefer(self.mate,individual)
            # 如果偏好求婚对象，那么修改自身的匹配对象为求婚对象，原匹配对象的匹配对象为None
            if who > 1:
                self.mate.mate = None
                self.mate = perfer_mate
                return True
            else:
                return False
        else:
            # 如果没有匹配对象，如果求婚者在偏好列表里，那么修改自身的匹配对象为求婚对象
            if individual.name in self.preference.keys():
                self.mate = individual
                return True
            else:
                return False

    def prefer(self,one,the_other):
        """ 比较one和the_other两者更偏好哪个

        :param Individual one: 个体一
        :param Individual the_other: 个体二
        :return: 返回偏好的对象及次序
        :rtype: tuple(Individual,int)
        """
        if self.preference.get(one.name) <= self.preference.get(the_other.name):
            return one,1
        return the_other,2

if __name__ == '__main__':
    m1 = Proposer(name='m1')
    m2 = Proposer(name='m2')
    m3 = Proposer(name='m3')
    m4 = Proposer(name='m4')
    m5 = Proposer(name='m5')

    w1 = Receiver(name='w1')
    w2 = Receiver(name='w2')
    w3 = Receiver(name='w3')
    w4 = Receiver(name='w4')

    m1.set_preference([w1,w2,w3,w4])
    m2.set_preference([w4,w2,w3,w1])
    m3.set_preference([w4,w3,w1,w2])
    m4.set_preference([w1,w4,w3,w2])
    m5.set_preference([w1,w2,w4])

    w1.set_preference([m2,m3,m1,m4,m5])
    w2.set_preference([m3,m1,m2,m4,m5])
    w3.set_preference([m5,m4,m1,m2,m3])
    w4.set_preference([m1,m4,m5,m2,m3])
    '''
    w2.make_proposal_to()
    print('********* Round One ***********')
    print(w2)
    print(m1)
    w1.make_proposal_to()
    print('********* Round Two ***********')
    print(w1)
    print(w2)
    print(m1)'''

    receiver = [w1,w2,w3,w4]
    proposer = [m1,m2,m3,m4,m5]
    check = True
    i = 1
    while(check):
        for pser in proposer:
            if pser.more_proposal:
                pser.make_proposal_to()
        print('Round: ',i)
        for r in receiver:
            if r.mate is None:
                mate = 'None'
            else:
                mate = r.mate.name
            print(r.name,' --- ',mate)
        check = any([p.more_proposal for p in proposer])
        i += 1
    print('-------Result-------')
    for item in proposer:
        if item.mate is None:
            mate = 'None'
        else:
            mate = item.mate.name
        print(item.name,' --- ',mate)


