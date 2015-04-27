from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'engine.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^helpdesk/', include('helpdesk.urls', namespace="helpdesk")),
    url(r'^regions/', include('regions.urls', namespace="regions")),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^search/', include('haystack.urls', namespace='search')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
