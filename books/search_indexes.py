# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2018/10/4 12:27
@desc: 用于Haystack确定应该在搜索索引中放置哪些数据并处理数据流的方式（创建索引）
"""

from haystack import indexes

from books.models import Book


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Book

    def index_queryset(self, using=None):
        return self.get_model().objects.all()