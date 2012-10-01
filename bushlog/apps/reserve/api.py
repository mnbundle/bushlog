from django.conf import settings

from tastypie import fields
from tastypie.resources import ModelResource

from bushlog.api.serializer import PrettyJSONSerializer, Serializer
from bushlog.apps.reserve.models import Reserve


class ReserveResource(ModelResource):
    sightings = fields.OneToManyField('bushlog.apps.sighting.api.SightingResource', 'sightings')

    class Meta:
        queryset = Reserve.objects.all()
        allowed_methods = ['get']
        excludes = ['id']
        serializer = PrettyJSONSerializer() if settings.DEBUG else Serializer()
