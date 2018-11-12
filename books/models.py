from django.db import models
from django.conf import settings
from django.urls import reverse

from users.models import UserProfile


class Category(models.Model):
    """
    分类表
    """
    name = models.CharField(max_length=32, verbose_name='分类名')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    图书表
    """
    name = models.CharField(max_length=128, verbose_name='书名')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 blank=True, null=True,
                                 related_name='category_books',
                                 verbose_name='分类')
    cover_picture = models.ImageField(upload_to='image/book/picture',
                                      default='image/default.jpg',
                                      verbose_name='封面图')
    desc = models.TextField(verbose_name='简介')
    upload_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='upload_books',
                                    verbose_name='上传者')
    pdf = models.FileField(upload_to='resource/pdf', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

    class Meta:
        verbose_name = '图书'
        verbose_name_plural = verbose_name
        ordering = ('-created',)

    def get_absolute_url(self):
        """
        :return: 图书绝对路径
        """
        return reverse('books:book_detail', args=[self.id])

    def __str__(self):
        return self.name



