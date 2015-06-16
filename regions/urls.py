from django.conf.urls import patterns, url

from regions import views

urlpatterns = patterns('',
    # ex: /regions/
    url(r'^$', views.index, name='index'),
    # ex: /regions/5/
    url(r'^(?P<region_id>\d+)/$', views.detail, name='detail'),
    url(r'^suggest_region/$', views.suggest_region, name='suggest_region'),
    url(r'^contact/(?P<contact_id>\d+)/edit/$', views.contact_modal, name='contact_edit_modal'),
    url(r'^(?P<region_id>\d+)/new_contact/$', views.contact_modal, name='new_contact_modal'),
)
