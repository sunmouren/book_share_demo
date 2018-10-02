# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/9/22 12:13
@desc: 
"""
from django.urls import path
from .views import UserProfileView, UserListView, FollowUserAjax


app_name = 'users'

urlpatterns = [
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('follow/', FollowUserAjax.as_view(), name='follow_user'),
]