from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.views import generic

from bushlog.apps.sighting.forms import CreateForm
from bushlog.apps.location.models import Coordinate
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
        Set the location and user associated to the sighting and set a success message if the form is valid.
        """
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.location = Coordinate.objects.create(
            latitude=form.cleaned_data.get('latitude', -21.987887),
            longitude=form.cleaned_data.get('longitude', 23.699001),
        )
        obj.save()

        print form.errors

        for image_id in form.cleaned_data.get('image_ids', '').split(','):
            try:
                image_obj = SightingImage.objects.get(id=image_id)
                image_obj.sighting = obj
                image_obj.save()
            except ValueError:
                pass

        messages.add_message(self.request, messages.SUCCESS, "Your sighting has been added.")

        return HttpResponseRedirect(reverse_lazy('sighting:index', args=[obj.reserve.slug, obj.species.slug, obj.id]))

    def form_invalid(self, form):
        """
        Set an error message if the form is invalid.
        """
        print form.errors
        messages.add_message(self.request, messages.ERROR, self.error_msg)
        return HttpResponseRedirect(self.error_url)


class SightingImageCreateView(generic.CreateView):
    model = SightingImage


index = IndexDetailView.as_view()
create = SightingCreateView.as_view()
create_image = SightingImageCreateView.as_view()
