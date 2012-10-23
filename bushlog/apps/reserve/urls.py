from django.conf.urls.defaults import patterns, url


# reserve specific url patterns
urlpatterns = patterns('bushlog.apps.reserve.views',
    url(r'(?P<slug>\S+)/$', 'index', name='index'),
)
