from django.conf.urls.defaults import patterns, url


# profile specific url patterns
urlpatterns = patterns('bushlog.apps.profile.views',
    url(r'signin/$', 'signin', name='signin'),
    url(r'signup/$', 'signup', name='signup'),
    url(r'signout/$', 'signout', name='signout'),
    url(r'validate/$', 'validate_unique', name='validate_unique'),
)
