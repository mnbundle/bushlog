from django.conf.urls import patterns, url, include

from rest_framework.urlpatterns import format_suffix_patterns


# static url patterns
urlpatterns = patterns('bushlog.api.views',
    url(r'^$', 'index')
)

# reserve api url patterns
urlpatterns += patterns('bushlog.api.views',
    url(r'^reserves/$', 'reserve_list', name='reserve_list'),
    url(r'^reserves/(?P<pk>\d+)/$', 'reserve_detail', name='reserve_detail')
)

# sighting api url patterns
urlpatterns += patterns('bushlog.api.views',
    url(r'^species/$', 'species_list', name='species_list'),
    url(r'^species/(?P<pk>\d+)/$', 'species_detail', name='species_detail')
)

# wildlife api url patterns
urlpatterns += patterns('bushlog.api.views',
    url(r'^sightingimages/$', 'sightingimage_list', name='sightingimage_list'),
    url(r'^sightingimages/(?P<pk>\d+)/$', 'sightingimage_detail', name='sightingimage_detail')
)

# format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
