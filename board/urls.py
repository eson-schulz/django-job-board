from django.conf.urls import include, url
from board import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^company/post-a-job/$', views.post_a_job, name='post_a_job'),

    url(r'^job/(?P<company_slug>[\w\-]+)/(?P<post_slug>[\w\-]+)/$', views.job_details, name='job_details'),
]


handler404 = 'board.views.page_not_found'