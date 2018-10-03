# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/10/3 10:51
@desc: 
"""
from django import forms

from .models import UserProfile


class UserLoginForm(forms.Form):
    """
    登录验证表单
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)


class UserRegisterForm(forms.Form):
    """
    注册验证表单
    """
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class ModifyUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'nickname', 'signature']
