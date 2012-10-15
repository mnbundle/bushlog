from django.conf.urls.defaults import patterns, url


# profile specific url patterns
urlpatterns = patterns('bushlog.apps.profile.views',
    url(r'signin/$', 'signin', name='signin'),
    url(r'signup/$', 'signup', name='signup'),
    url(r'update/$', 'update', name='update'),
    url(r'reset-password/$', 'reset_password', name='reset_password'),
    url(r'signout/$', 'signout', name='signout'),
    url(r'validate/(?P<type>\w+)/$', 'validate', name='validate'),
)
