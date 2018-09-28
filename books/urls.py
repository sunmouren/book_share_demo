# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/9/22 12:01
@desc: 
"""

from django.urls import path

from .views import BookListView, BookDetailView


app_name = 'books'

urlpatterns = [
    path('list/', BookListView.as_view(), name='book_list'),
    path('detail/<int:book_id>/', BookDetailView.as_view(), name='book_detail'),
]
