from django.conf.urls.defaults import patterns, url

# profile specific url patterns
urlpatterns = patterns('bushlog.apps.profile.views',
    url(r'login/$', 'login', name='login'),
)
