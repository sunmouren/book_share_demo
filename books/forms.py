# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/10/5 16:59
@desc: 
"""

from django import forms

from .models import Book


class UploadBookForm(forms.ModelForm):
    """
    上传图书验证表单
    """
    class Meta:
        model = Book
        fields = ['cover_picture', 'name', 'desc', 'category']