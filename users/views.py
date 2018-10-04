from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import UserProfile, FollowUser
from .forms import UserLoginForm, UserRegisterForm, ModifyUserProfileForm


class CustomBackend(ModelBackend):
    """
    增加邮箱登录
    继承ModelBackend类，覆盖authenticate方法, 增加邮箱认证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 使用get是因为不希望用户存在两个, Q：使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            # 判断密码是否匹配时，django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有check_password(self, raw_password)方法
            if user.check_password(password):
                return user
        except BaseException as e:
            return None


class UserLoginView(View):
    """
    登录
    """
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            user_email = request.POST.get('email', None)
            password = request.POST.get('password', None)
            # 成功返回user对象，反之返回None, 这里在前面已经增加邮箱登录，所以可以直接把当作username进行登录。
            user = authenticate(username=user_email, password=password)
            if user is not None:
                login(request, user)
                # 如果登录成功，则重定向到个人主页
                return HttpResponseRedirect(reverse('users:user_profile', args=[user.id]))
            else:
                return render(request, 'login.html', {
                    'msg': '邮箱或密码出错',
                    'user_login_form': user_login_form})
        else:
            invalid_keys = [key for key in user_login_form.errors]
            return render(request, 'login.html', {
                'user_login_form': user_login_form,
                'invalid_keys': invalid_keys})


class UserLogoutView(View):
    """
    退出登录
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class UserRegisterView(View):
    """
    注册
    """
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        user_register_form = UserRegisterForm(request.POST)
        print(user_register_form)
        if user_register_form.is_valid():
            user_email = request.POST.get('email', None)
            password1 = request.POST.get('password1', None)
            password2 = request.POST.get('password2', None)
            username = user_email.split('@')[0]

            if not password1 == password2:
                return render(request, 'register.html', {'msg': '密码不一致'})
            if UserProfile.objects.filter(username=username):
                return render(request, 'register.html', {'msg': '用户已存在'})
            # 实例化一个UserProfile对象，并进行相应的赋值
            new_user = UserProfile(username=username, email=user_email)
            # 对保存到数据库的密码加密
            new_user.password = make_password(password1)
            new_user.save()
            return render(request, 'register.html', {'status': 'ok'})
        else:
            invalid_keys = [key for key in user_register_form.errors]
            return render(request, 'register.html', {
                'user_register_form': user_register_form,
                'invalid_keys': invalid_keys,
            })


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


class UserListView(View):
    """
    书友列表
    """
    def get(self, request):
        # 当前页面
        current_page = 'user_list'
        users = UserProfile.objects.order_by('-date_joined')
        return render(request, 'user-list.html', {'users': users, 'current_page': current_page})


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


class ModifyUserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(UserProfile, id=int(user_id))
        check_is_owner(request, user)
        modify_form = ModifyUserProfileForm(instance=user)
        return render(request, 'modify-user-profile.html', {
            'user': user,
            'modify_from': modify_form,
        })

    def post(self, request, user_id):
        user = get_object_or_404(UserProfile, id=int(user_id))
        check_is_owner(request, user)
        modify_form = ModifyUserProfileForm(instance=user, data=request.POST, files=request.FILES)
        if modify_form.is_valid():
            modify_form.save()
            return render(request, 'modify-user-profile.html', {
                'user': user,
                'status': 'ok',
            })
        else:
            return render(request, 'modify-user-profile.html', {
                'user': user,
                'modify_from': modify_form,
                'status': 'ko',
            })


def check_is_owner(request, user):
    """
    检查是否为当前所有者
    :param request:
    :param user:
    :return:
    """
    if not request.user == user:
        raise Http404





