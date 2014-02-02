from django.contrib.auth.models import User

from rest_framework import serializers

from bushlog.apps.profile.models import UserProfile
from bushlog.apps.reserve.models import Reserve
from bushlog.apps.sighting.models import Sighting, SightingImage
from bushlog.apps.wildlife.models import Species, SpeciesInfo


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['biography', 'avatar', 'gender']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'profile']


class ReserveSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.Field()
    species = serializers.ManyHyperlinkedRelatedField(view_name='api:species_detail')
    bounds = serializers.Field(source='bounds')
    bounding_box = serializers.Field(source='bounding_box')
    resource_url = serializers.HyperlinkedIdentityField(view_name='api:reserve_detail')

    class Meta:
        model = Reserve
        fields = ['id', 'name', 'slug', 'description', 'website', 'species', 'bounds', 'bounding_box', 'resource_url']


class SightingImageSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.Field()
    exif_data = serializers.Field(source='exif_data')
    gps_data = serializers.Field(source='gps_data')
    resource_url = serializers.HyperlinkedIdentityField(view_name='api:sightingimage_detail')

    class Meta:
        model = SightingImage
        fields = ['id', 'image', 'exif_data', 'gps_data', 'resource_url']


class SightingSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.Field()
    user = serializers.HyperlinkedRelatedField(view_name='api:user_detail')
    reserve = serializers.HyperlinkedRelatedField(view_name='api:reserve_detail')
    species = serializers.HyperlinkedRelatedField(view_name='api:species_detail')
    images = serializers.HyperlinkedRelatedField(view_name='api:sightingimage_detail', many=True)
    mapdata = serializers.CharField(source='mapdata', read_only=True)
    resource_url = serializers.HyperlinkedIdentityField(view_name='api:sighting_detail')

    class Meta:
        model = Sighting
        fields = [
            'id', 'user', 'reserve', 'species', 'images', 'date_of_sighting', 'description', 'mapdata', 'resource_url'
        ]


class SpeciesInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SpeciesInfo
        fields = ['height', 'length', 'mass', 'horn_length']


class SpeciesSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.Field()
    similiar_species = serializers.ManyHyperlinkedRelatedField(view_name='api:species_detail')
    female_info = SpeciesInfoSerializer()
    male_info = SpeciesInfoSerializer()
    resource_url = serializers.HyperlinkedIdentityField(view_name='api:species_detail')

    class Meta:
        model = Species
        fields = [
            'id', 'public', 'common_name', 'scientific_name', 'slug', 'classification', 'general_info',
            'similiar_species', 'female_info', 'male_info', 'marker', 'resource_url'
        ]
