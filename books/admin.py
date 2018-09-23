from django.contrib import admin

from .models import Category, Book


class CategoryAdmin(admin.ModelAdmin):
    """
    分类管理后台
    """
    list_display = ['name']
    list_filter = ['name']


class BookAdmin(admin.ModelAdmin):
    """
    图书后台管理
    """
    list_display = ['name', 'upload_user', 'created']
    list_filter = ['name', 'upload_user', 'created']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
