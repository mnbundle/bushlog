from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

from bushlog.api.serializers import ReserveSerializer, SpeciesSerializer, SightingSerializer, SightingImageSerializer, UserSerializer
from bushlog.apps.reserve.models import Reserve
from bushlog.apps.sighting.models import Sighting, SightingImage
from bushlog.apps.wildlife.models import Species


@api_view(['GET'])
def index(request, format=None):
    """
    The entry endpoint of the entire API.
    """
    return Response({
        'reserves': reverse('api:reserve_list', request=request),
        'species': reverse('api:species_list', request=request),
        'sighting': reverse('api:sighting_list', request=request),
        'sightingimage': reverse('api:sightingimage_list', request=request),
        'user': reverse('api:user_list', request=request),
    })


# userprofile views
class UserListAPIView(generics.ListAPIView):
    """
    API endpoint that represents a list of reserves.
    """
    model = User
    serializer_class = UserSerializer


class UserDetailAPIView(generics.RetrieveAPIView):
    """
    API endpoint that represents a reserve's details.
    """
    model = User
    serializer_class = UserSerializer


user_list = UserListAPIView.as_view()
user_detail = UserDetailAPIView.as_view()


# reserve views
class ReserveListAPIView(generics.ListAPIView):
    """
    API endpoint that represents a list of reserves.
    """
    model = Reserve
    serializer_class = ReserveSerializer

    def get_queryset(self):
        queryset = Reserve.objects.all()
        name = self.request.QUERY_PARAMS.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class ReserveDetailAPIView(generics.RetrieveAPIView):
    """
    API endpoint that represents a reserve's details.
    """
    model = Reserve
    serializer_class = ReserveSerializer


reserve_list = ReserveListAPIView.as_view()
reserve_detail = ReserveDetailAPIView.as_view()


# sighting views
class SightingListAPIView(generics.ListAPIView):
    """
    API endpoint that represents a list of sightings.
    """
    model = Sighting
    serializer_class = SightingSerializer

    def get_queryset(self):
        queryset = Sighting.objects.all()

        reserve = self.request.QUERY_PARAMS.get('reserve')
        species = self.request.QUERY_PARAMS.get('species')
        user = self.request.QUERY_PARAMS.get('user')

        if reserve:
            queryset = queryset.filter(reserve__id=reserve)
        if species:
            queryset = queryset.filter(species__id=species)
        if user:
            queryset = queryset.filter(species__id=user)

        return queryset


class SightingDetailAPIView(generics.RetrieveAPIView):
    """
    API endpoint that represents a sighting image's details.
    """
    model = Sighting
    serializer_class = SightingSerializer


# sighting views
class SightingImageListAPIView(generics.ListAPIView):
    """
    API endpoint that represents a list of sighting images.
    """
    model = SightingImage
    serializer_class = SightingImageSerializer


class SightingImageDetailAPIView(generics.RetrieveAPIView):
    """
    API endpoint that represents a sighting image's details.
    """
    model = SightingImage
    serializer_class = SightingImageSerializer


sighting_list = SightingListAPIView.as_view()
sighting_detail = SightingDetailAPIView.as_view()
sightingimage_list = SightingImageListAPIView.as_view()
sightingimage_detail = SightingImageDetailAPIView.as_view()


# wildlife views
class SpeciesListAPIView(generics.ListAPIView):
    """
    API endpoint that represents a list of species.
    """
    model = Species
    serializer_class = SpeciesSerializer

    def get_queryset(self):
        queryset = Species.objects.all()
        name = self.request.QUERY_PARAMS.get('name')
        if name:
            queryset = queryset.filter(common_name__icontains=name)
        return queryset


class SpeciesDetailAPIView(generics.RetrieveAPIView):
    """
    API endpoint that represents a species's details.
    """
    model = Species
    serializer_class = SpeciesSerializer


species_list = SpeciesListAPIView.as_view()
species_detail = SpeciesDetailAPIView.as_view()
