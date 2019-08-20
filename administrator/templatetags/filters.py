# 自定义过滤器
# 过滤器的本质其实就是python中的函数
from django.template import Library

from administrator.models import *

# 创建一个library类的对象
register = Library()


# 自定义过滤器至少有一个参数，最多2个
# 将函数装饰成python中的过滤器进行使用
def get_doctor(depart_ment):
    '''
    获取科室对应的医生的信息
    :param depart_ment:
    :return:
    '''
    a = UserInfo.objects.filter(doctor_belong__depart_name=depart_ment)#用户表的医生所属科室和科室表
    # print(depart_ment)
    print("a",a)
    # print(depart_ment,a.count())
    return a


register.filter("get_doctor", get_doctor)


def get_doctor_count(depart_ment):
    '''
    获取科室对应的医生的数据的条数
    :param depart_ment:
    :return:
    '''
    b = UserInfo.objects.filter(doctor_belong__depart_name=depart_ment).count() + 1
    # print('--'*100)
    # print("医生管理_各个科室对应的数据数",b)
    return b


register.filter("get_doctor_count", get_doctor_count)


def get_user(u_role_name):
    '''
    获取角色对应的用户信息
    :param u_role_name:
    :return:
    '''
    c=UserInfo.objects.filter(user_role__role_name=u_role_name)
    return c

register.filter("get_user", get_user)


def get_user_count(u_role_name):
    '''
    获取角色对应的用户的数据的条数
    :param u_role_name:
    :return:
    '''
    d=UserInfo.objects.filter(user_role__role_name=u_role_name).count() + 1
    # print('用户管理表_角色',u_role_name)
    # print('*'*100)
    # print('用户管理表_各个角色对应的数据条数',d)
    return d

register.filter("get_user_count", get_user_count)