from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic

from bushlog.apps.profile.forms import SignInForm, SignUpForm


class SignInView(generic.FormView):
    template_name = 'signin.html'
    form_class = SignInForm
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
            return self.form_invalid(form)

        user = authenticate(username=user.username, password=password)

        if user is not None:
            if not user.is_active:
                messages.add_message(self.request, messages.ERROR, "Your account seems to have been deactivated.")
                return HttpResponseRedirect(reverse('index'))
            else:
                login(self.request, user)
        else:
            return self.form_invalid(form)

        return HttpResponseRedirect(reverse('index'))

    def form_invalid(self, form):
        """
        Set an error message if the form is valid.
        """
        messages.add_message(self.request, messages.ERROR, self.error_msg)
        return HttpResponseRedirect(reverse('index'))


class SignUpView(generic.FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
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
            return self.form_invalid(form)

        user = authenticate(username=user.username, password=password)

        if user is not None:
            if not user.is_active:
                messages.add_message(self.request, messages.ERROR, "Your account seems to have been deactivated.")
                return HttpResponseRedirect(reverse('index'))
            else:
                login(self.request, user)
        else:
            return self.form_invalid(form)

        return HttpResponseRedirect(reverse('index'))

    def form_invalid(self, form):
        """
        Set an error message if the form is valid.
        """
        messages.add_message(self.request, messages.ERROR, self.error_msg)
        return HttpResponseRedirect(reverse('index'))


class SignOutView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self):
        logout(self.request)
        return reverse('index')


signin = SignInView.as_view()
signout = SignOutView.as_view()
signup = SignUpView.as_view()

