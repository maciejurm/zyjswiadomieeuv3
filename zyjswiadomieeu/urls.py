"""zyjswiadomieeu URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('taggit/', include('taggit_selectize.urls')),
    path('account/', include('account.urls')),
    path('blog/', include('blog.urls', namespace='blog'), name='blog'),
    path('books/', include('books.urls', namespace='books'), name='books'),
    path('events/', include('events.urls', namespace='events'), name='events'),
    path('api/', include('likedislike.urls', namespace='api'), name='api'),
    path('tinymce/', include('tinymce.urls')),
    path('kontakt/', TemplateView.as_view(template_name="statyczne/contact.html"), name='contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
