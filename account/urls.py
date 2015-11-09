from django.conf.urls import url
import views

# How the url patterns are structured:
# company/ - All things used by the company
# jobs/ - All things for users to look at - Jobs, Companies, etc
# search/ - Search functions for different features of the website

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^update/$', views.update_info, name='update_info'),

]