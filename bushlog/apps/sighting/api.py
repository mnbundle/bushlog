from django.conf import settings

from tastypie import fields
from tastypie.resources import ModelResource

from bushlog.api.serializer import PrettyJSONSerializer, Serializer
from bushlog.apps.sighting.models import Sighting


class SightingResource(ModelResource):
    #user = fields.ForeignKey('bushlog.apps.profile.api.ProfileResource', 'location')
    location = fields.ForeignKey('bushlog.apps.location.api.CoordinateResource', 'location', full=True)
    reserve = fields.ForeignKey('bushlog.apps.reserve.api.ReserveResource', 'reserve')
    species = fields.ForeignKey('bushlog.apps.wildlife.api.SpeciesResource', 'species')

    class Meta:
        queryset = Sighting.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        excludes = ['id']
        filtering = {
            'with_young': ['exact'],
            'with_kill': ['exact'],
            'estimated_number': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        serializer = PrettyJSONSerializer() if settings.DEBUG else Serializer()
