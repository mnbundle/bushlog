from django.conf.urls import patterns, url


# sighting specific url patterns
urlpatterns = patterns('bushlog.apps.sighting.views',
    url(r'^search/$', 'search', name='search'),
    url(r'^create/$', 'create', name='create'),
    url(r'^create/image/$', 'create_image', name='create_image'),
    url(r'^forms/(?P<type>\w+)/$', 'forms', name='forms'),
    url(r'^activate/(?P<pk>\d+)/$', 'activate', name='activate'),
    url(r'^deactivate/(?P<pk>\d+)/$', 'deactivate', name='deactivate'),
    url(r'^latest/$', 'latest', name='latest'),
    url(r'^(?P<reserve_slug>\S+)/(?P<species_slug>\S+)/(?P<pk>\d+)/$', 'detail', name='detail'),
    url(r'^(?P<reserve_slug>\S+)/(?P<species_slug>\S+)/$', 'list', name='list')
)
