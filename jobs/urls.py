"""jobs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.conf import settings
from django.views.generic.base import RedirectView
from board.views import employers_only_index
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^account/', include('account.urls')),

    url(r'^tinymce/', include('tinymce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.EMPLOYERS_ONLY:
    urlpatterns += [
        url(r'^launch/', include('board.urls')),
        url(r'^$', employers_only_index, name='employers_only_index'),
    ]
else:
    urlpatterns += [
        url(r'^', include('board.urls')),
        url(r'^launch/', RedirectView.as_view(url='/', permanent=True), name='old_launch')
    ]