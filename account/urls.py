from django.conf.urls import url
from django.contrib.auth.views import password_reset, password_reset_confirm, password_change
import views

# How the url patterns are structured:
# company/ - All things used by the company
# jobs/ - All things for users to look at - Jobs, Companies, etc
# search/ - Search functions for different features of the website

urlpatterns = [

    url(r'^register/$', views.register, name='register'),
    url(r'^update/$', views.update_info, name='update_info'),
    url(r'^logout/$', views.company_logout, name='logout'),
    url(r'^login/$', views.company_login, name='login'),
    url(r'^password-reset/$', password_reset, {'template_name': 'account/password/password_reset.html'}, name='password_reset'),
    url(r'^password-reset/done/$', views.password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, {'template_name': 'account/password/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', views.password_reset_complete, name='password_reset_complete'),

    url(r'^password-change/$', password_change, {'template_name': 'account/password/password_change.html'}, name='password_change'),
    url(r'^password-change/done/$', views.password_change_complete, name='password_change_done'),

    url(r'^company/post-a-job/$', views.post_a_job, name='post_a_job'),
    url(r'^update-posts/$', views.update_posts_base, name='update_posts'),
    url(r'^update-posts/(?P<post_slug>[\w\-]+)/$', views.post_a_job, name='update_post'),
]