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
    hot_comments = Comment.objects.all()
    return hot_comments
