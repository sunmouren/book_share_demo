# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/9/28 20:17
@desc: 
"""

from django.urls import path

from .views import SubmitCommentAjax, LikeCommentAjax, DeleteCommentAJax

app_name = 'comments'

urlpatterns = [
    path('submit/', SubmitCommentAjax.as_view(), name='submit_comment'),
    path('like/', LikeCommentAjax.as_view(), name='submit_like'),
    path('delete/', DeleteCommentAJax.as_view(), name='submit_delete'),
]