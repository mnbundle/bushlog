from django.conf.urls import patterns, url


# sighting specific url patterns
urlpatterns = patterns('bushlog.apps.sighting.views',
    url(r'(?P<reserve_slug>\S+)/(?P<species_slug>\S+)/(?P<pk>\d+)/$', 'index', name='index'),
    url(r'create/$', 'create', name='create'),
    url(r'create/image$', 'create_image', name='create_image'),
)
