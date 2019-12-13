from django.conf.urls import include, url
from organizations import views

app_name = 'orgs'

urlpatterns = [
    url('^$', views.orgs, name='orgs'),
    url(r'^(?P<org_id>\d+)/$', views.one_org, name='one_org'),
]
