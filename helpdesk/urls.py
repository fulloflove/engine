from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from helpdesk import views

urlpatterns = patterns('',
    url(r'^$', views.my_open_issues, name='index'),
    url(r'^my/$', views.my_open_issues, name='my'),
    url(r'^my/closed/$', views.my_closed_issues, name='my_recent_closed'),
    url(r'^my/closed/period/$', views.my_issues_period, name='my_issues_period'),
    url(r'^all/$', views.all_open_issues, name='all'),
    url(r'^all/closed/$', views.all_closed_issues, name='all_recent_closed'),
    url(r'^all/closed/period/$', views.all_issues_period, name='all_issues_period'),

    url(r'^region/(?P<region_id>\d+)/closed/$', views.closed_issues_by_region, name='region_closed'),
    url(r'^region/(?P<region_id>\d+)/closed/period/$', views.closed_issues_by_region_period,
        name='region_closed_period'),
    url(r'^region/(?P<region_id>\d+)/$', views.open_issues_by_region, name='region_open'),

    url(r'^project/(?P<project_id>\d+)/closed/$', views.closed_issues_by_project, name='project_closed'),
    url(r'^project/(?P<project_id>\d+)/closed/period/$', views.closed_issues_by_project_period,
        name='project_closed_period'),
    url(r'^project/(?P<project_id>\d+)/$', views.open_issues_by_project, name='project_open'),

    url(r'^service_type/(?P<service_type_id>\d+)/closed/$', views.closed_issues_by_service_type,
        name='service_type_closed'),
    url(r'^service_type/(?P<service_type_id>\d+)/closed/period/$', views.closed_issues_by_service_type_period,
        name='service_type_closed_period'),
    url(r'^service_type/(?P<service_type_id>\d+)/$', views.open_issues_by_service_type, name='service_type_open'),

    url(r'^filter/$', views.filter_issues, name='filter'),

    url(r'^user/(?P<assignee_id>\d+)/closed/$', views.closed_issues_by_assignee, name='assignee_closed'),
    url(r'^user/(?P<assignee_id>\d+)/closed/period/$', views.closed_issues_by_assignee_period,
        name='assignee_closed_period'),
    url(r'^user/(?P<assignee_id>\d+)/$', views.open_issues_by_assignee, name='assignee_open'),

    url(r'^issue/(?P<issue_id>\d+)/status/(?P<status_id>\d)/$', views.issue_status, name='issue_status'),
    url(r'^issue/(?P<issue_id>\d+)/edit/$', views.edit_issue, name='edit_issue'),
    url(r'^issue/(?P<issue_id>\d+)/$', views.issue, name='issue'),

    url(r'^new_issue/$', views.new_issue, name='new_issue'),
    url(r'^popover/$', views.popover, name='popover'),
    url(r'^popover/(?P<region_id>\d+)/$', views.popover, name='popover_with_reg'),

    url(r'^accounts/$', views.accounts, name='accounts'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'helpdesk:index'}, name='logout'),
    url(r'^edit_account/$', views.account_change, name='edit_account'),
    url(r'^change_password/$', auth_views.password_change,
        {'template_name': 'registration/change_password.html',
        'post_change_redirect': 'helpdesk:index'},
        name='change_password'),

    url(r'^test/(?P<issue_id>\d+)/$', views.test, name='test'),
)