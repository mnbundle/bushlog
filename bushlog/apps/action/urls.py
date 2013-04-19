from django.conf.urls import patterns, url


# profile specific url patterns
urlpatterns = patterns('bushlog.apps.action.views',
    url(r'^like/(?P<type>\w+)/$', 'like', name='like'),
)
