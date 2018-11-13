from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from utils.checks import check_is_owner

from .models import Book, Category
from .forms import UploadBookForm


class UploadBookView(LoginRequiredMixin, View):
    """
    上传图书
    """
    def get(self, request):
        upload_form = UploadBookForm()
        categories = Category.objects.all()
        return render(request, 'upload-book.html', {
            'upload_form': upload_form,
            'categories': categories,
        })

    def post(self, request):
        upload_form = UploadBookForm(data=request.POST, files=request.FILES)
        if upload_form.is_valid():
            try:
                new_book = upload_form.save(commit=False)
                new_book.upload_user = request.user
                new_book.save()
                return HttpResponseRedirect(reverse('users:user_profile', args=[request.user.id]))
            except BaseException as e:
                print('upload error {0}'.format(e))
        categories = Category.objects.all()
        invalid_keys = [key for key in upload_form.errors]
        return render(request, 'upload-book.html', {
            'upload_form': upload_form,
            'categories': categories,
            'invalid_keys': invalid_keys,
            'status': 'ko',
        })


class EditBookView(LoginRequiredMixin, View):
    """
    编辑修改图书
    """
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=int(book_id))
        check_is_owner(request, book.upload_user)
        categories = Category.objects.all()
        return render(request, 'edit-book.html', {
            'book': book,
            'categories': categories,
        })

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=int(book_id))
        check_is_owner(request, book.upload_user)
        categories = Category.objects.all()
        # 因为编辑的验证表单和上传的验证表单一样，所以直接使用。
        edit_form = UploadBookForm(instance=book, data=request.POST, files=request.FILES)
        if edit_form.is_valid():
            edit_form.save()
            return render(request, 'edit-book.html', {
                'book': book,
                'categories': categories,
                'status': 'ok',
            })
        else:
            invalid_keys = [key for key in edit_form.errors]
            return render(request, 'edit-book.html', {
                'book': book,
                'edit_form': edit_form,
                'categories': categories,
                'invalid_keys': invalid_keys,
                'status': 'ko',

            })


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

        fake_books = [1, 2, 3, 4, 5]

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


class BookDetailView(View):
    """
    图书详情页面
    """
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=int(book_id))
        data = request.GET.get('data', 'recent')
        comments, info = self.get_comments(book, data)
        return render(request, 'book-detail.html', {
            'book': book,
            'comments': comments,
            'comment_count': len(comments),
            'info': info,
            'data': data,
        })

    def get_comments(self, book, data):
        """
        :param book:
        :param data:
        :return: 如果data==recent则返回最新书评，如果data==hot则返回精彩评论，其他情况则返回[]
        """
        if data == 'recent':
            comments = book.comments.order_by('-created')
            info = '最新'
        elif data == 'hot':
            # 可根据书评点赞书进行降序排序
            comments = book.comments.exclude(like_number=0).order_by('-like_number')
            info = '精彩'
        else:
            comments = []
            info = '暂无'
        return comments, info


class PreviewPdfView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=int(book_id))
        return render(request, 'preview-pdf.html', {'book': book})
