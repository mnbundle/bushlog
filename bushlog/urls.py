from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views import generic

from tastypie.api import Api

from bushlog.apps.location.api import CoordinateResource
from bushlog.apps.profile.api import UserResource
from bushlog.apps.reserve.api import ReserveResource
from bushlog.apps.sighting.api import SightingResource
from bushlog.apps.wildlife.api import SpeciesResource, SpeciesInfoResource

# set admin to autodiscover registered admin classes
admin.autodiscover()

# instantiate the api
v1_api = Api(api_name='v1')

# register api resources
v1_api.register(CoordinateResource())
v1_api.register(ReserveResource())
v1_api.register(SightingResource())
v1_api.register(SpeciesResource())
v1_api.register(SpeciesInfoResource())
v1_api.register(UserResource())

# static url patterns
urlpatterns = patterns('',
    url(r'^$', generic.TemplateView.as_view(template_name="index.html"), name='index')
)

# admin url patterns
urlpatterns += patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls))
)

# api urls
urlpatterns += patterns('',
    url(r'^api/', include('bushlog.api.urls'))
)

# user profile url patterns
urlpatterns += patterns('',
    url(r'^profile/', include('bushlog.apps.profile.urls', namespace='profile'))
)

# reserve url patterns
urlpatterns += patterns('',
    url(r'^reserve/', include('bushlog.apps.reserve.urls', namespace='reserve'))
)

# wildlife url patterns
urlpatterns += patterns('',
    url(r'^wildlife/', include('bushlog.apps.wildlife.urls', namespace='wildlife'))
)

# comments framework patterns
urlpatterns += patterns('',
    (r'^comments/', include('django.contrib.comments.urls'))
)

# social auth urls
urlpatterns += patterns('',
    url(r'social/', include('social_auth.urls'))
)

# serves static file while DEBUG is true
urlpatterns += staticfiles_urlpatterns()

# serves media files in development
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media\/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^templates\/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.TEMPLATE_DIRS[0]})
    )
