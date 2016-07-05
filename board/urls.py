from django.conf.urls import url
from django.conf import settings
from board import views

# How the url patterns are structured:
# company/ - All things used by the company
# jobs/ - All things for users to look at - Jobs, Companies, etc
# search/ - Search functions for different features of the website

urlpatterns = [
    # The company details of any company
    url(r'^jobs/(?P<company_slug>[\w\-]+)/$', views.company_details, name='company_details'),

    # The job details of any job
    url(r'^jobs/(?P<company_slug>[\w\-]+)/(?P<post_slug>[\w\-]+)/$', views.job_details, name='job_details'),

    # General information for employers
    url(r'^employers/$', views.company_info, name='company_info'),

    url(r'^employers/jobs/$', views.company_plans, name='company_plans'),

    # About us page
    url(r'^about-us/$', views.about_us, name='about_us'),

    # Contact us page
    url(r'^contact-us/$', views.contact_us, name='contact_us'),

    # FAQ
    url(r'^faq/$', views.faq, name='faq'),

    # Terms of Service
    url(r'^terms/$', views.tos, name='tos'),

    # Privacy Policy
    url(r'^privacy-policy/$', views.privacy_policy, name='privacy'),
]

# We want to display different urls without breaking them if we are in pre-launch mode
if settings.EMPLOYERS_ONLY:
    urlpatterns += [
        url(r'^$', views.employers_only_search, name='index'),
        url(r'^search/category/(?P<category_slug>[\w\-]+)/$', views.not_viewable_launch, name='category_search'),
        url(r'^search/job-types/(?P<job_type_slug>[\w\-]+)/$', views.not_viewable_launch, name='job_type_search'),
        url(r'^search/categories/$', views.not_viewable_launch, name='category_list'),
        url(r'^search/companies/$', views.not_viewable_launch, name='company_list'),
    ]
else:
    urlpatterns += [
        url(r'^$', views.index, name='index'),

        # Search function for categories
        url(r'^search/category/(?P<category_slug>[\w\-]+)/$', views.index, name='category_search'),

        # Search function for job types
        url(r'^search/job-types/(?P<job_type_slug>[\w\-]+)/$', views.index, name='job_type_search'),

        # The category list page
        url(r'^search/categories/$', views.categories, name='category_list'),

        # The company list page
        url(r'^search/companies/$', views.company_list, name='company_list'),
    ]


handler404 = 'board.views.page_not_found'
