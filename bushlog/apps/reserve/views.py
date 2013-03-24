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

        try:
            reserve = [obj for obj in Reserve.objects.all() if obj.sighting_in_reserve(coordinates)][0]
            return {
                'id': reserve.id,
                'name': reserve.name
            }
        except IndexError:
            return None


index = IndexDetailView.as_view()
search_point = SearchPointView.as_view()
