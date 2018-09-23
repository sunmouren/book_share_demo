from django.contrib import admin

from users.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    """
    用户后台管理
    """
    list_display = ['username', 'email', 'date_joined']
    list_filter = ['username', 'email', 'date_joined']


admin.site.register(UserProfile, UserProfileAdmin)