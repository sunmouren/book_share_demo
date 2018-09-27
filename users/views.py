from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from .models import UserProfile


class UserProfileView(View):
    def get(self, request, user_id):
        user = get_object_or_404(UserProfile, id=int(user_id))
        return render(request, 'user-profile.html', {
            'user': user,
        })
