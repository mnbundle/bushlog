from django.conf import settings

from tastypie.resources import ModelResource

from bushlog.api.serializer import PrettyJSONSerializer, Serializer
from bushlog.apps.location.models import Coordinate


class CoordinateResource(ModelResource):
    class Meta:
        queryset = Coordinate.objects.all()
        allowed_methods = ['get']
        excludes = ['id']
        serializer = PrettyJSONSerializer() if settings.DEBUG else Serializer()
