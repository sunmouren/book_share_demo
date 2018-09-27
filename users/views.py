from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from .models import UserProfile


class UserProfileView(View):
    """
    用户个人主页
    """
    def get(self, request, user_id):
        user = get_object_or_404(UserProfile, id=int(user_id))
        is_owner = '我' if request.user == user else 'TA'
        data = request.GET.get('data', 'books')
        books = self.get_books(data, user)
        comments = self.get_comments(data, user)
        print(books)
        print(comments)

        return render(request, 'user-profile.html', {
            'user': user,
            'books': books,
            'comments': comments,
            'is_owner': is_owner,
            'data': data,
        })

    def get_books(self, data, user):
        return user.upload_books.all() if data == 'books' else None

    def get_comments(self, data, user):
        return user.book_comments.all() if data == 'comments' else None

