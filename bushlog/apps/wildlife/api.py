from django.conf import settings

from tastypie import fields
from tastypie.resources import ModelResource

from bushlog.api.serializer import PrettyJSONSerializer, Serializer
from bushlog.apps.wildlife.models import Species, SpeciesInfo


class SpeciesInfoResource(ModelResource):
    class Meta:
        queryset = SpeciesInfo.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        excludes = ['id']
        serializer = PrettyJSONSerializer() if settings.DEBUG else Serializer()


class SpeciesResource(ModelResource):
    sightings = fields.OneToManyField('bushlog.apps.sighting.api.SightingResource', 'sightings')
    female_info = fields.ForeignKey(SpeciesInfoResource, 'female_info', full=True)
    male_info = fields.ForeignKey(SpeciesInfoResource, 'male_info', full=True)
    similiar_species = fields.ManyToManyField('self', 'similiar_species')

    class Meta:
        queryset = Species.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        excludes = ['marker', 'slug']
        serializer = PrettyJSONSerializer() if settings.DEBUG else Serializer()
