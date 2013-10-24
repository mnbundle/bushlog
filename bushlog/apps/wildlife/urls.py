from django.conf.urls import patterns, url


# wildlife specific url patterns
urlpatterns = patterns('bushlog.apps.wildlife.views',
    url(r'^$', 'list', name='list'),
    url(r'^(?P<slug>\S+)/$', 'detail', name='detail'),
)
