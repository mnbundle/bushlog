from django.conf import settings
from django.contrib import messages
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.views import generic

from bushlog.apps.sighting.forms import CreateForm
from bushlog.apps.location.models import Coordinate
from bushlog.apps.sighting.models import Sighting, SightingImage


class IndexDetailView(generic.DetailView):
    model = Sighting

    def render_to_response(self, context, **response_kwargs):
        """
        Ensure only public sightings are served unless the user is the owner of this sighting.
        """
        if (self.object.user == self.request.user) or self.object.public:
            return super(IndexDetailView, self).render_to_response(context, **response_kwargs)
        raise Http404

    def get_queryset(self):
        return self.model.objects.filter(
            reserve__slug=self.kwargs.get('reserve_slug'),
            species__slug=self.kwargs.get('species_slug')
        )


class SearchListView(generic.ListView):
    model = Sighting
    template_name = 'sighting/sighting_search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)

        latitude = self.request.GET.get('latitude')
        longitude = self.request.GET.get('longitude')
        if latitude and longitude:
            context['coordinates'] = {
                'latitude': latitude,
                'longitude': longitude
            }

        return context


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

        for image_id in form.cleaned_data.get('image_ids', '').split(','):
            try:
                image_obj = SightingImage.objects.get(id=image_id)
                image_obj.sighting = obj
                image_obj.save()
            except ValueError:
                pass

        # XXX hacked in until report listing is done
        mail_admins(
            "Sighting Added", "A new sighting has been added and may need modiration: %s%s" % (
                settings.HOST, obj.get_absolute_url()
            ), fail_silently=True
        )

        messages.add_message(self.request, messages.SUCCESS, "Your sighting has been added.")

        return HttpResponseRedirect(obj.get_absolute_url())

    def form_invalid(self, form):
        """
        Set an error message if the form is invalid.
        """
        messages.add_message(self.request, messages.ERROR, self.error_msg)
        return HttpResponseRedirect(self.error_url)


class SightingImageCreateView(generic.CreateView):
    model = SightingImage


class FormsView(generic.TemplateView):
    template_name = 'sighting/forms.html'

    def get_context_data(self, **kwargs):
        context = super(FormsView, self).get_context_data(**kwargs)
        context.update({
            'type': kwargs.get('type')
        })

        return context


index = IndexDetailView.as_view()
search = SearchListView.as_view()
create = SightingCreateView.as_view()
create_image = SightingImageCreateView.as_view()
forms = FormsView.as_view()
