# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/9/22 12:13
@desc: 
"""
from django.urls import path
from .views import UserProfileView


app_name = 'users'

urlpatterns = [
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
]