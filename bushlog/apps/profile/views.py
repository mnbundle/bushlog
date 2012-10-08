from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic

from bushlog.apps.profile.forms import SignInForm, SignUpForm
from bushlog.apps.profile.decorators import json_response


class SignInFormView(generic.FormView):
    template_name = "signin.html"
    form_class = SignInForm
    success_url = reverse('index')
    error_url = reverse('index')
    error_msg = "Your login details were entered incorrectly. Please try again."

    def form_valid(self, form):
        """
        Set a success message if the form is valid.
        """
        username_email = form.data.get('username_email')
        password = form.data.get('password')
        remember_me = form.data.get('remember_me', False)

        try:
            user = User.objects.get(email=username_email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username_email)
            except User.DoesNotExist:
                return self.form_invalid(form)

        user = authenticate(username=user.username, password=password)

        if user is not None:
            if not user.is_active:
                messages.add_message(self.request, messages.ERROR, "Your account seems to have been deactivated.")
                return HttpResponseRedirect(self.error_url)
            else:
                if not remember_me:
                    self.request.session.set_expiry(0)
                login(self.request, user)
        else:
            return self.form_invalid(form)

        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        """
        Set an error message if the form is invalid.
        """
        print form.data
        messages.add_message(self.request, messages.ERROR, self.error_msg)
        return HttpResponseRedirect(self.error_url)


class SignUpFormView(generic.FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse('index')
    error_url = reverse('index')
    error_msg = "The signup process failed. Please try again."

    def form_valid(self, form):
        """
        Set a success message if the form is valid.
        """
        user = form.save()
        user.set_password(form.data.get('password'))
        user.save()

        if user:
            messages.add_message(
                self.request, messages.SUCCESS,
                "Thank you for signing up. An email has been sent to you with details to complete your registration."
            )
            return HttpResponseRedirect(self.success_url)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        """
        Set an error message if the form is invalid.
        """
        messages.add_message(self.request, messages.ERROR, self.error_msg)
        return HttpResponseRedirect(self.error_url)


class SignOutRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self):
        logout(self.request)
        return reverse('index')


class ValidateUniqueView(generic.View):

    @json_response
    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        email = request.GET.get('email')

        try:
            if username:
                User.objects.get(username=username)
            elif email:
                User.objects.get(email=email)
        except User.DoesNotExist:
            return True
        return False


signin = SignInFormView.as_view()
signup = SignUpFormView.as_view()
signout = SignOutRedirectView.as_view()
validate_unique = ValidateUniqueView.as_view()
