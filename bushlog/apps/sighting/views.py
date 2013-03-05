from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.views import generic

from bushlog.apps.sighting.models import Sighting


class IndexDetailView(generic.DetailView):
    model = Sighting


class SightingCreateView(generic.CreateView):
    model = Sighting


index = IndexDetailView.as_view()
create = SightingCreateView.as_view()
