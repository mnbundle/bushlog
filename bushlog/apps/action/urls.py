from django.conf.urls import patterns, url


# profile specific url patterns
urlpatterns = patterns('bushlog.apps.action.views',
    url(r'^like/(?P<type>\w+)/$', 'like', name='like'),
    url(r'^comment/(?P<type>\w+)/(?P<pk>\d+)/$', 'comment', name='comment'),
    url(r'^comment/(?P<type>\w+)/$', 'comment', name='comment')
)
