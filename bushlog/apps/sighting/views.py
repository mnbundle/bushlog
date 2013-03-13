from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.views import generic

from bushlog.apps.sighting.forms import CreateForm
from bushlog.apps.sighting.models import Sighting, SightingImage


class IndexDetailView(generic.DetailView):
    model = Sighting


class SightingCreateView(generic.CreateView):
    model = Sighting
    form_class = CreateForm
    form_prefix = "sighting_create"
    error_url = reverse_lazy('index')
    error_msg = "Saving your sighting failed. Please try again."

    def render_to_response(self, context, **response_kwargs):
        """
        Ensure only ajax requests are allowed to render this view.
        """
        if self.request.is_ajax():
            return super(SightingCreateView, self).render_to_response(context, **response_kwargs)
        return HttpResponseBadRequest()

    def get_form_kwargs(self):
        kwargs = super(generic.CreateView, self).get_form_kwargs()
        if self.form_prefix:
            kwargs.update({'prefix': self.form_prefix})
        return kwargs

    def form_valid(self, form):
        """
        Set a success message if the form is valid.
        """
        obj = form.save()

        for image_id in self.request.POST.get('image_ids').split(','):
            image_obj = SightingImage.objects.get(id=image_id)
            image_obj.sighting = obj
            image_obj.save()

        messages.add_message(self.request, messages.SUCCESS, "Your sighting has been added.")

        return reverse_lazy('sighting:index', args=[obj.reserve.slug, obj.species.slug, obj.id])

    def form_invalid(self, form):
        """
        Set an error message if the form is invalid.
        """
        messages.add_message(self.request, messages.ERROR, self.error_msg)
        return HttpResponseRedirect(self.error_url)


class SightingImageCreateView(generic.CreateView):
    model = SightingImage


index = IndexDetailView.as_view()
create = SightingCreateView.as_view()
create_image = SightingImageCreateView.as_view()
