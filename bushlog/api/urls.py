from django.conf.urls.defaults import patterns, include, url

from tastypie.api import NamespacedApi

from bushlog.apps.location.api import CoordinateResource
from bushlog.apps.profile.api import UserResource
from bushlog.apps.reserve.api import ReserveResource
from bushlog.apps.sighting.api import SightingResource, SightingImageResource
from bushlog.apps.wildlife.api import SpeciesResource, SpeciesInfoResource

# instantiate the api
v1_api = NamespacedApi(api_name='v1.0', urlconf_namespace='api')

# register api resources
v1_api.register(CoordinateResource())
v1_api.register(ReserveResource())
v1_api.register(SightingResource())
v1_api.register(SightingImageResource())
v1_api.register(SpeciesResource())
v1_api.register(SpeciesInfoResource())
v1_api.register(UserResource())

# api urls
urlpatterns = patterns('',
    url(r'^', include(v1_api.urls)),
)
