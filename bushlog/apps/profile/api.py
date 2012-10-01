from django.conf import settings

from tastypie import fields
from tastypie.resources import ModelResource

from bushlog.api.serializer import PrettyJSONSerializer, Serializer
from bushlog.apps.profile.models import User


class UserResource(ModelResource):
    sightings = fields.OneToManyField('bushlog.apps.sighting.api.SightingResource', 'sightings')

    class Meta:
        queryset = User.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        fields = ['username', 'date_joined']
        serializer = PrettyJSONSerializer() if settings.DEBUG else Serializer()
