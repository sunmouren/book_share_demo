from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from .models import UserProfile


class UserProfileView(View):
    """
    用户个人主页
    """
    def get(self, request, user_id):
        user = get_object_or_404(UserProfile, id=int(user_id))
        info = '我' if request.user == user else 'TA'
        data = request.GET.get('data', 'books')
        books = self.get_books(user, data)
        comments = self.get_comments(data, user)

        return render(request, 'user-profile.html', {
            'user': user,
            'books': books,
            'comments': comments,
            'info': info,
            'data': data,
        })

    def get_books(self, user, data):
        return user.upload_books.all() if data == 'books' else []

    def get_comments(self, user, data):
        return user.book_comments.all() if data == 'comments' else []

