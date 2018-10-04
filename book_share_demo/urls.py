"""book_share_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    # index
    path('', TemplateView.as_view(template_name='index.html', extra_context={'current_page': ''}), name='index'),
    # users
    path('user/', include('users.urls', namespace='users')),
    # books
    path('book/', include('books.urls', namespace='books')),
    # comments
    path('comment/', include('comments.urls', namespace='comments')),
    # search
    path('search/', include('haystack.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
