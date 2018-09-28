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
    avatar = models.ImageField(upload_to='image/user/avatar',
                               default='image/default.jpg', verbose_name='头像')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        """
        :return: 用户绝对路径
        """
        return reverse('users:user_profile', args=[self.id])

    def __str__(self):
        if self.nickname:
            return self.nickname
        else:
            return self.username


