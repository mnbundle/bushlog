from django.conf.urls import patterns, url


# reserve specific url patterns
urlpatterns = patterns('bushlog.apps.reserve.views',
    url(r'^$', 'list', name='list'),
    url(r'^search-point/$', 'searchpoint', name='searchpoint'),
    url(r'^(?P<slug>\S+)/dashboard/$', 'dashboard', name='dashboard'),
    url(r'^(?P<slug>\S+)/$', 'detail', name='detail'),
)
