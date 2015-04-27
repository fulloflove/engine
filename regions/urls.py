from django.conf.urls import patterns, url

from regions import views

urlpatterns = patterns('',
    # ex: /regions/
    url(r'^$', views.index, name='index'),
    # ex: /regions/5/
    url(r'^(?P<region_id>\d+)/$', views.detail, name='detail'),
    # ex: /regions/5/edit/
    url(r'^(?P<region_id>\d+)/edit/$', views.edit, name='edit'),
    # ex: /regions/5/submit/
    url(r'^(?P<region_id>\d+)/submit/$', views.submit, name='submit'),
    url(r'^suggest_region/$', views.suggest_region, name='suggest_region'),
)
