from django.shortcuts import render
from django.views.generic import View


class UserProfileView(View):
    def get(self, request):
        return render(request, 'book-list.html')
