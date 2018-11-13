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
        fields = ['cover_picture', 'pdf', 'name', 'desc', 'category']

    def clean_cover_picture(self):
        cover_picture = self.cleaned_data['cover_picture']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = cover_picture.name.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('请选择格式为jpg、jpeg、png的图片!')
        return cover_picture

    def clean_pdf(self):
        pdf = self.cleaned_data['pdf']
        extension = pdf.name.rsplit('.', 1)[1].lower()
        if extension != 'pdf':
            raise forms.ValidationError('请选择格式为pdf的电子书书')
        return pdf