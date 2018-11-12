# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/9/22 12:01
@desc: 
"""

from django.urls import path

from .views import BookListView, BookDetailView, UploadBookView, EditBookView, PreviewPdfView


app_name = 'books'

urlpatterns = [
    path('upload/', UploadBookView.as_view(), name='upload_book'),
    path('<int:book_id>/edit/', EditBookView.as_view(), name='edit_book'),
    path('list/', BookListView.as_view(), name='book_list'),
    path('detail/<int:book_id>/', BookDetailView.as_view(), name='book_detail'),
    path('preview/pdf/<int:book_id>/', PreviewPdfView.as_view(), name='preview_pdf'),
]
