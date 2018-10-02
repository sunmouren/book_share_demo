from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import UserProfile, FollowUser


class UserProfileView(View):
    """
    用户个人主页
    """
    def get(self, request, user_id):
        user = get_object_or_404(UserProfile, id=int(user_id))
        info = '我' if request.user == user else 'TA'
        data = request.GET.get('data', 'books')
        books = self.get_books(user, data)
        comments = self.get_comments(user, data)
        followings = self.get_followings(user, data)
        followers = self.get_followers(user, data)

        return render(request, 'user-profile.html', {
            'user': user,
            'books': books,
            'comments': comments,
            'followings': followings,
            'followers': followers,
            'info': info,
            'data': data,
        })

    def get_books(self, user, data):
        return user.upload_books.all() if data == 'books' else []

    def get_comments(self, user, data):
        return user.book_comments.all() if data == 'comments' else []

    def get_followings(self, user, data):
        return user.following_users.all() if data == 'followings' else []

    def get_followers(self, user, data):
        return user.follower_users.all() if data == 'followers' else []


class UserListView(LoginRequiredMixin, View):
    """
    书友列表
    """
    def get(self, request):
        users = UserProfile.objects.order_by('-date_joined')
        return render(request, 'user-list.html', {'users': users})


class FollowUserAjax(LoginRequiredMixin, View):
    """
    关注用户，允许条件，用户已登录，post请求
    """
    def post(self, request):
        user_id = request.POST.get('uid', None)
        action = request.POST.get('action', None)
        if user_id and action:
            try:
                user = UserProfile.objects.get(id=int(user_id))
                # Ps: 如果前端避免不了关注自己，那么我就不客气了，我还不信治不了你了，接招吧~
                if request.user == user:
                    return JsonResponse({'msg': 'ko'})

                if action == 'follow':
                    FollowUser.objects.get_or_create(user_from=request.user, user_to=user)
                else:
                    FollowUser.objects.filter(user_from=request.user, user_to=user).delete()

                return JsonResponse({'msg': 'ok'})
            except UserProfile.DoesNotExist:
                return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


