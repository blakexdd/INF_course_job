"""course_job URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from course_job import views
from django.conf.urls import include, url

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^$', views.home, name='index'),
    url(r'^login/$', views.page_login, name='login'),
    url(r'^logout/$', views.page_logout, name='logout'),
    url(r'^organizations/', include('organizations.urls', namespace='orgs')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^create_org$', views.create_organizations, name='create_organization'),
    url(r'^create_person$', views.create_person, name='create_person'),
    url(r'^edit_days$', views.creating_day, name='create_day'),
    url(r'^delete_org$', views.delete_organization, name='delete_organization'),
    url(r'^delete_pers$', views.delete_person, name='delete_person'),
    url(r'delete_day$', views.delete_day, name='delete_day'),
    url(r'^org_edit$', views.edit_organization, name='edit_organization'),
    url(r'^edit_person$', views.edit_person, name='edit_person'),
    url(r'edit_day$', views.edit_days, name='edit_day')
]
