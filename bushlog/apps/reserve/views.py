from django.views import generic

from bushlog.apps.reserve.models import Reserve
from bushlog.decorators import json_response


class IndexDetailView(generic.DetailView):
    model = Reserve


class SearchPointView(generic.View):

    @json_response
    def get(self, request, *args, **kwargs):
        coordinates = {
            'latitude': request.GET.get('latitude'),
            'longitude': request.GET.get('longitude')
        }

        for reserve in Reserve.objects.all():
            if reserve.sighting_in_reserve(coordinates):
                return {
                    'id': reserve.id,
                    'name': reserve.name
                }

        return None


index = IndexDetailView.as_view()
search_point = SearchPointView.as_view()
