from django.views import generic

from bushlog.apps.reserve.models import Reserve
from bushlog.decorators import json_response


class IndexDetailView(generic.DetailView):
    model = Reserve


class SerachPointView(generic.View):

    @json_response
    def get(self, request, type, *args, **kwargs):
        pass


index = IndexDetailView.as_view()
search_point = SerachPointView.as_view()
