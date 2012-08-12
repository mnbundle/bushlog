from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic

from bushlog.apps.profile.forms import LoginForm


class LoginView(generic.FormView):
    template_name = 'login.html'
    form_class = LoginForm
    error_msg = "Your login details were entered incorrectly. Please try again."

    def get_success_url(self):
        """
        Redirect to the previous url.
        """
        return HttpResponseRedirect(reverse('index'))

    def form_valid(self, form):
        """
        Set a success message if the form is valid.
        """
        email = form.data.get('email')
        password = form.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            if not user.check_password(password):
                messages.add_message(self.request, messages.ERROR, self.error_msg)
                return HttpResponseRedirect(reverse('index'))
            if not user.is_active:
                messages.add_message(self.request, messages.ERROR, "Your account seems to have been deactivated.")
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.add_message(self.request, messages.ERROR, self.error_msg)
            return HttpResponseRedirect(reverse('index'))

        return HttpResponseRedirect(reverse('index'))

    def form_invalid(self, form):
        """
        Set an error message if the form is valid.
        """
        messages.add_message(self.request, messages.ERROR, self.error_msg)
        return HttpResponseRedirect(reverse('index'))


login = LoginView.as_view()
