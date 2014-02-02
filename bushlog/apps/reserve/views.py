from django.views import generic

from bushlog.apps.reserve.models import Reserve
from bushlog.decorators import json_response


class ListView(generic.ListView):
    model = Reserve


class DetailView(generic.DetailView):
    model = Reserve


class DashboardDetailView(generic.DetailView):
    model = Reserve
    template_name = 'reserve/reserve_detail_dashboard.html'


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


list = ListView.as_view()
detail = DetailView.as_view()
dashboard = DashboardDetailView.as_view()
searchpoint = SearchPointView.as_view()
