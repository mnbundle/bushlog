from django.conf.urls import patterns, url


# profile specific url patterns
urlpatterns = patterns('bushlog.apps.like.views',
    url(r'^(?P<type>\w+)/$', 'create', name='create'),
)
