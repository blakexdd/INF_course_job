from django.conf.urls import include, url
from organizations import views

app_name = 'orgs'

urlpatterns = [
    url('^$', views.orgs, name='orgs'),
    url(r'^(?P<user_id>\d)+/$', views.pers_cabinet, name='pers_cabinet'),
]

