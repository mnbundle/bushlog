from django.views import generic

from bushlog.apps.reserve.models import Reserve


class IndexDetailView(generic.DetailView):
    model = Reserve


index = IndexDetailView.as_view()
