from django.conf.urls import url
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
    url(r'^company/post-a-job/$', views.post_a_job, name='post_a_job'),
    url(r'^update-posts/$', views.update_posts_base, name='update_posts'),
    url(r'^update-posts/(?P<post_slug>[\w\-]+)/$', views.update_post, name='update_post'),
]