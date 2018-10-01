# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/9/23 16:48
@desc: 
"""
from django import template

from ..models import Comment


register = template.Library()


@register.simple_tag
def get_hot_comments():
    """
    获取热门评论
    :return:
    """
    return Comment.objects.all().order_by('-created')[:2]


@register.simple_tag
def check_is_liked_comment(request, comment):
    """
    检查当前用户是否在喜欢书评列表中
    :param request:
    :param comment:
    :return:
    """
    return request.user in comment.like_user.all()
