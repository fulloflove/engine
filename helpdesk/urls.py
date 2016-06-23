from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from helpdesk import views

urlpatterns = patterns('',
    url(r'^$', views.issues_main_view, {'active_nav': 'my'}, name='index'),

    url(r'^(?P<active_nav>(my|all|region|project|service_type|user))'
        '(?:/(?P<item_id>\d+))?(?:/(?P<status>(closed|any)))?(?:/(?P<scope>period))?/$',
        views.issues_main_view, name='issues_main_view'),

     url(r'^my/$', views.issues_main_view, {'active_nav': 'my'}, name='my'),
     url(r'^all/$', views.issues_main_view, {'active_nav': 'all'}, name='all'),

     url(r'^filter/$', views.filter_issues, name='filter'),

    url(r'^issue/(?P<issue_id>\d+)/status/(?P<status_id>\d)/$', views.issue_status, name='issue_status'),
    url(r'^issue/(?P<issue_id>\d+)/edit/$', views.edit_issue, name='edit_issue'),
    url(r'^issue/(?P<issue_id>\d+)/$', views.issue, name='issue'),

    url(r'^new_issue/$', views.new_issue, name='new_issue'),
    url(r'^popover/$', views.popover, name='popover'),
    url(r'^popover/(?P<region_id>\d+)/$', views.popover, name='popover_with_reg'),

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'helpdesk:index'}, name='logout'),
    url(r'^edit_account/$', views.account_change, name='edit_account'),
    url(r'^change_password/$', auth_views.password_change,
        {'template_name': 'registration/change_password.html',
        'post_change_redirect': 'helpdesk:index'},
        name='change_password'),
)