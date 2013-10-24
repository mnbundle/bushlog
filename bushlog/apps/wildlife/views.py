from django.views import generic

from bushlog.apps.wildlife.models import Species


class ListView(generic.ListView):
    model = Species


class DetailView(generic.DetailView):
    model = Species


list = ListView.as_view()
detail = DetailView.as_view()
