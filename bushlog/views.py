from django.contrib import messages
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
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
        form.send()
        messages.add_message(
            self.request, messages.SUCCESS,
            "Thank you for reporting this issue. We will try and resolve it as soon as possible."
        )
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        """
        Set an error message if the form is invalid.
        """
        messages.add_message(self.request, messages.ERROR, self.error_msg)
        return HttpResponseRedirect(self.error_url)


class CSRFFailureTemplateView(generic.View):
    """
    Return a custom 403 error page and notify admins of the failure.
    """
    def post(self, request, *args, **kwargs):
        print str(request.POST)
        mail_admins(
            "CSRF Error", "A CSRF Error was thrown. The following data was sent: %s" % (str(request.POST)),
            fail_silently=True
        )
        return render_to_response('403.html', {}, RequestContext(request))


support = SupportFormView.as_view()
csrf_failure = CSRFFailureTemplateView.as_view()
