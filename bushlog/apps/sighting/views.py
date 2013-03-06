from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.views import generic

from bushlog.apps.sighting.models import Sighting, SightingImage


class IndexDetailView(generic.DetailView):
    model = Sighting


class SightingCreateView(generic.CreateView):
    model = Sighting

    def form_valid(self, form):
        obj = form.save()

        for image_id in self.request.POST.get('image_ids').split(','):
            image_obj = SightingImage.objects.get(id=image_id)
            image_obj.sighting = obj
            image_obj.save()

        return super(SightingCreateView, self).form_valid(form)


class SightingImageCreateView(generic.CreateView):
    model = SightingImage


index = IndexDetailView.as_view()
create = SightingCreateView.as_view()
create_image = SightingImageCreateView.as_view()
