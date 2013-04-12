from django.conf.urls import patterns, url


# profile specific url patterns
urlpatterns = patterns('bushlog.apps.profile.views',
    url(r'^signin/$', 'signin', name='signin'),
    url(r'^signup/$', 'signup', name='signup'),
    url(r'^update/$', 'update', name='update'),
    url(r'^avatar/$', 'avatar', name='avatar'),
    url(r'^forgot-password/$', 'forgot_password', name='forgot_password'),
    url(r'^reset-password/$', 'reset_password', name='reset_password'),
    url(r'^reset-password-redirect/$', 'reset_password_redirect', name='reset_password_redirect'),
    url(r'^resend-activation/$', 'resend_activation', name='resend_activation'),
    url(r'^activate/$', 'activate', name='activate'),
    url(r'^signout/$', 'signout', name='signout'),
    url(r'^validate/(?P<type>\w+)/$', 'validate', name='validate'),
    url(r'^associate/$', 'associate', name='associate'),
    url(r'^inactive/$', 'inactive', name='inactive'),
    url(r'^forms/(?P<type>\w+)/$', 'forms', name='forms'),
    url(r'^(?P<slug>\S+)/$', 'index', name='index'),
)
