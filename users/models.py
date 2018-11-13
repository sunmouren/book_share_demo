from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class UserProfile(AbstractUser):
    """
    用户表
    """
    nickname = models.CharField(max_length=30, blank=True,
                                null=True, verbose_name='昵称')
    signature = models.CharField(max_length=128, blank=True,
                                 null=True, verbose_name='个性签名', default='这家伙很懒，什么都没有留下！')
    following_users = models.ManyToManyField('self', through='FollowUser',
                                             related_name='follower_users',
                                             symmetrical=False)
    avatar = models.ImageField(upload_to='image/user/avatar',
                               default='image/default.jpg', verbose_name='头像')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('users:user_profile', args=[self.id])

    @property
    def get_books(self):
        return self.upload_books.all()

    @property
    def get_comments(self):
        return self.book_comments.all()

    @property
    def get_followings(self):
        return self.following_users.all()

    @property
    def get_followers(self):
        return self.follower_users.all()

    def __str__(self):
        if self.nickname:
            return self.nickname
        else:
            return self.username


class FollowUser(models.Model):
    """
    关注用户表
    """
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='rel_from_set')
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = '关注'
        verbose_name_plural = verbose_name
        ordering = ('-created',)

    def __str__(self):
        return '{0} 关注了 {1}'.format(self.user_from, self.user_to)



