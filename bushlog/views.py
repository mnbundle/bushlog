from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic

from bushlog.forms import SupportForm


class SupportFormView(generic.FormView):
    template_name = "support.html"
    form_class = SupportForm
    success_url = reverse_lazy('support')
    error_url = reverse_lazy('support')
    error_msg = "Issue report failed. Please try again."
    form_prefix = "support"

    def get_form_kwargs(self):
        kwargs = super(generic.FormView, self).get_form_kwargs()
        if self.form_prefix:
            kwargs.update({'prefix': self.form_prefix})
        return kwargs

    def form_valid(self, form):
        """
        Set a success message if the form is valid.
        """
        if form.send():
            messages.add_message(
                self.request, messages.SUCCESS,
                "An email has been sent with instructions to reset your password."
            )
            return HttpResponseRedirect(self.success_url)
        return self.form_invalid(form)

    def form_invalid(self, form):
        """
        Set an error message if the form is invalid.
        """
        messages.add_message(self.request, messages.ERROR, self.error_msg)
        return HttpResponseRedirect(self.error_url)


support = SupportFormView.as_view()
