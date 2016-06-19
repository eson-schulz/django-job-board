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

    # Search function for job types
    url(r'^search/job-types/(?P<job_type_slug>[\w\-]+)/$', views.index, name='job_type_search'),

    # The category list page
    url(r'^search/categories/$', views.categories, name='category_list'),

    # The company list page
    url(r'^search/companies/$', views.company_list, name='company_list'),

    # The company details of any company
    url(r'^jobs/(?P<company_slug>[\w\-]+)/$', views.company_details, name='company_details'),

    # The job details of any job
    url(r'^jobs/(?P<company_slug>[\w\-]+)/(?P<post_slug>[\w\-]+)/$', views.job_details, name='job_details'),

    # General information for employers
    url(r'^employers/$', views.company_plans, name='company_plans'),

    # About us page
    url(r'^about-us/$', views.about_us, name='about_us'),

    # Contact us page
    url(r'^contact-us/$', views.contact_us, name='contact_us'),
]

handler404 = 'board.views.page_not_found'
