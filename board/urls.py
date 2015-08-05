from django.conf.urls import url
from board import views

# How the url patterns are structured:
# company/ - All things used by the company
# jobs/ - All things for users to look at - Jobs, Companies, etc
# search/ - Search functions for different features of the website

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # Search function for categories
    url(r'^search/category/(?P<category_slug>[\w\-]+)/$', views.index, name='category_search'),

    # For employers to post a job
    url(r'^company/post-a-job/$', views.post_a_job, name='post_a_job'),

    # The company details of any company
    url(r'^jobs/(?P<company_slug>[\w\-]+)/$', views.company_details, name='company_details'),

    # The job details of any job
    url(r'^jobs/(?P<company_slug>[\w\-]+)/(?P<post_slug>[\w\-]+)/$', views.job_details, name='job_details'),
]


handler404 = 'board.views.page_not_found'