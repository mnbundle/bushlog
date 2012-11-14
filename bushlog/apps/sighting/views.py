from django.views import generic

from bushlog.apps.sighting.models import Sighting


class IndexDetailView(generic.DetailView):
    model = Sighting


index = IndexDetailView.as_view()
