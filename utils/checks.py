# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/10/5 20:29
@desc: 
"""
from django.http import Http404


def check_is_owner(request, user):
    """
    检查是否为当前所有者
    :param request:
    :param user:
    :return:
    """
    if not request.user == user:
        raise Http404