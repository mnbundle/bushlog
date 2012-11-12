from django.views import generic

from bushlog.apps.wildlife.models import Species


class IndexDetailView(generic.DetailView):
    model = Species


index = IndexDetailView.as_view()
