from django.shortcuts import render
from django.views.generic import View

from .models import Book, Category


class BookListView(View):
    """
    图书列表
    """
    def get(self, request):
        # 当前页面
        current_page = 'book_list'
        # 取出所有图书
        books = Book.objects.all()
        # 取出所有图书分类
        categories = Category.objects.all()

        # 获取前端传入的分类id, 默认0是全部分类
        current_category_id = request.GET.get('category', 0)

        fake_books = [1, 2]

        if current_category_id:
            books = books.filter(category_id=int(current_category_id))
            # 家测试图书数据
            fake_books = list(range(0, len(books) * 10))

        return render(request, 'book-list.html', {
            'books': books,
            'fake_books': fake_books,
            'categories': categories,
            'current_page': current_page,
            'current_category_id': current_category_id,
        })
