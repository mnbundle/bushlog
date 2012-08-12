from tastypie import fields
from tastypie.resources import ModelResource, ALL

from bushlog.apps.reserve.models import Reserve
from bushlog.apps.sighting.models import Sighting
from bushlog.apps.wildlife.models import Species


class ReserveResource(ModelResource):
    class Meta:
        queryset = Reserve.objects.all()
        allowed_methods = ['get']


class SpeciesResource(ModelResource):
    class Meta:
        queryset = Species.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        excludes = ['marker', 'slug']


class SightingResource(ModelResource):
    reserve = fields.ForeignKey(ReserveResource, 'reserve')

    class Meta:
        queryset = Sighting.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
            'reserve': ALL,
            'with_young': ['exact'],
            'with_kill': ['exact'],
            'estimated_number': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
