from django.conf.urls import patterns, url


# reserve specific url patterns
urlpatterns = patterns('bushlog.apps.reserve.views',
    url(r'^search-point/$', 'search_point', name='search_point'),
    url(r'^(?P<slug>\S+)/$', 'index', name='index'),
)
