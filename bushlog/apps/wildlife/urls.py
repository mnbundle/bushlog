from django.conf.urls import patterns, url


# wildlife specific url patterns
urlpatterns = patterns('bushlog.apps.wildlife.views',
    url(r'(?P<slug>\S+)/$', 'index', name='index'),
)
