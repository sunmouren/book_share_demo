# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/9/23 15:25
@desc: 
"""

from django import template

from ..models import UserProfile


register = template.Library()


@register.simple_tag
def get_recommend_users():
    """
    获取推荐用户，测试阶段，仅获取部分用户
    :return:
    """
    users = UserProfile.objects.all()
    return users


