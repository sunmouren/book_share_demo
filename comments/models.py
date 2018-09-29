from django.db import models
from django.conf import settings

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

from books.models import Book


class Comment(MPTTModel):
    """
    多级书评表
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='book_comments', verbose_name='评论者')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True,
                             related_name='comments', verbose_name='图书')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                            related_name='replies', verbose_name='父级书评')
    content = models.TextField(verbose_name='评论内容', default=None)
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments',
                                       blank=True)
    like_number = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='评论时间')

    class MPTTMeta:
        order_insertion_by = ('-created', )

    class Meta:
        verbose_name = '书评'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.parent is not None:
            return '{0} 回复 {1}'.format(self.user.username, self.parent.user.username)
        else:
            return '{0} 评论了 {1}'.format(self.user.username, self.book)