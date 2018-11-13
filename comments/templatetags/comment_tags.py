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
    获取各个图书最热门书评
    :return:
    """
    comments = Comment.objects.exclude(like_number=0).order_by('-like_number')
    book_ids, comment_ids = [], []
    for comment in comments:
        if comment.book.id in book_ids:
            comment_ids.append(comment.id)
            continue
        book_ids.append(comment.book.id)
    return comments.exclude(id__in=comment_ids)


@register.simple_tag
def check_is_liked(request, comment):
    """
    检查当前用户是否在喜欢书评列表中
    :param request:
    :param comment:
    :return:
    """
    return request.user in comment.like_user.all()
