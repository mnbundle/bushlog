from django.conf.urls import patterns, url


# profile specific url patterns
urlpatterns = patterns('bushlog.apps.profile.views',
    url(r'signin/$', 'signin', name='signin'),
    url(r'signup/$', 'signup', name='signup'),
    url(r'update/$', 'update', name='update'),
    url(r'reset-password/$', 'reset_password', name='reset_password'),
    url(r'resend-activation/$', 'resend_activation', name='resend_activation'),
    url(r'signout/$', 'signout', name='signout'),
    url(r'validate/(?P<type>\w+)/$', 'validate', name='validate'),
    url(r'associate/$', 'associate', name='associate'),
    url(r'inactive/$', 'inactive', name='inactive'),
    url(r'(?P<slug>\S+)/$', 'index', name='index'),
)
