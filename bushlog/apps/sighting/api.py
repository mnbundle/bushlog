from django.conf import settings
from django.conf.urls.defaults import url

from tastypie import fields
from tastypie.resources import ModelResource

from bushlog.api.serializer import PrettyJSONSerializer, Serializer
from bushlog.apps.sighting.models import Sighting, SightingImage


class SightingResource(ModelResource):
    location = fields.ForeignKey('bushlog.apps.location.api.CoordinateResource', 'location', full=True)
    reserve = fields.ForeignKey('bushlog.apps.reserve.api.ReserveResource', 'reserve')
    species = fields.ForeignKey('bushlog.apps.wildlife.api.SpeciesResource', 'species')

    class Meta:
        queryset = Sighting.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        api_name = "sighting_sighting"
        filtering = {
            'with_young': ['exact'],
            'with_kill': ['exact'],
            'estimated_number': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        serializer = PrettyJSONSerializer() if settings.DEBUG else Serializer()


class SightingImageResource(ModelResource):
    sighting = fields.ForeignKey('bushlog.apps.sighting.api.SightingResource', 'sighting', null=True, blank=True)

    class Meta:
        queryset = SightingImage.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
            'with_young': ['exact'],
            'with_kill': ['exact'],
            'estimated_number': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        serializer = PrettyJSONSerializer() if settings.DEBUG else Serializer()
