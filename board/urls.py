from django.conf.urls import include, url
from board import views

urlpatterns = [
    url(r'^', views.index, name='index'),
]


handler404 = 'board.views.page_not_found'