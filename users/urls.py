# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/9/22 12:13
@desc: 
"""
from django.urls import path
from .views import UserProfileView, UserListView, FollowUserAjax,\
    UserLoginView, UserRegisterView, UserLogoutView, ModifyUserProfileView


app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('follow/', FollowUserAjax.as_view(), name='follow_user'),
    path('<int:user_id>/modify/', ModifyUserProfileView.as_view(), name='modify_profile'),
]