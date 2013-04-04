from rest_framework import serializers

from bushlog.apps.reserve.models import Reserve
from bushlog.apps.sighting.models import SightingImage
from bushlog.apps.wildlife.models import Species, SpeciesInfo


class ReserveSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.Field()
    species = serializers.ManyHyperlinkedRelatedField(view_name='api:species_detail')
    site_url = serializers.HyperlinkedIdentityField(view_name='reserve:index')
    resource_url = serializers.HyperlinkedIdentityField(view_name='api:reserve_detail')

    class Meta:
        model = Reserve
        fields = ['id', 'name', 'description', 'website', 'species', 'site_url', 'resource_url']


class SightingImageSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.Field()
    exif_data = serializers.Field(source='exif_data')
    gps_data = serializers.Field(source='gps_data')
    resource_url = serializers.HyperlinkedIdentityField(view_name='api:sightingimage_detail')

    class Meta:
        model = SightingImage
        fields = ['id', 'image', 'exif_data', 'gps_data', 'resource_url']


class SpeciesInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SpeciesInfo
        fields = ['height', 'length', 'mass', 'horn_length']


class SpeciesSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.Field()
    similiar_species = serializers.ManyHyperlinkedRelatedField(view_name='api:species_detail')
    female_info = SpeciesInfoSerializer()
    male_info = SpeciesInfoSerializer()
    site_url = serializers.HyperlinkedIdentityField(view_name='wildlife:index')
    resource_url = serializers.HyperlinkedIdentityField(view_name='api:species_detail')

    class Meta:
        model = Species
        fields = [
            'id', 'common_name', 'scientific_name', 'classification', 'general_info', 'similiar_species', 'female_info',
            'male_info', 'marker', 'site_url', 'resource_url'
        ]
