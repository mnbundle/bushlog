from django.conf.urls.defaults import patterns, include, url

from tastypie.api import Api

from bushlog.apps.location.api import CoordinateResource
from bushlog.apps.profile.api import UserResource
from bushlog.apps.reserve.api import ReserveResource
from bushlog.apps.sighting.api import SightingResource
from bushlog.apps.wildlife.api import SpeciesResource, SpeciesInfoResource

# instantiate the api
v1_api = Api(api_name='v1')

# register api resources
v1_api.register(CoordinateResource())
v1_api.register(ReserveResource())
v1_api.register(SightingResource())
v1_api.register(SpeciesResource())
v1_api.register(SpeciesInfoResource())
v1_api.register(UserResource())

# api urls
urlpatterns = patterns('',
    url(r'^', include(v1_api.urls)),
)
