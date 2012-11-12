from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.views import generic

from bushlog.apps.profile.decorators import json_response
from bushlog.apps.profile.forms import ResetPasswordForm, SignInForm, SignUpModelForm, UpdateModelForm, ResendActivationForm
from bushlog.apps.profile.models import UserProfile


class IndexDetailView(generic.DetailView):
    model = UserProfile


class SignInFormView(generic.FormView):
    template_name = "profile/signin.html"
    form_class = SignInForm
    error_url = reverse_lazy('index')
    error_msg = "Your login details were entered incorrectly. Please try again."
    form_prefix = "signin"

    def render_to_response(self, context, **response_kwargs):
        """
        Ensure only ajax requests are allowed to render this view.
        """
        if self.request.is_ajax():
            return super(SignInFormView, self).render_to_response(context, **response_kwargs)
        return HttpResponseBadRequest()

    def get_form_kwargs(self):
        kwargs = super(generic.FormView, self).get_form_kwargs()
        if self.form_prefix:
            kwargs.update({'prefix': self.form_prefix})
        return kwargs

    def form_valid(self, form):
        """
        Set a success message if the form is valid.
        """
        username_email = form.cleaned_data.get('username_email')
        password = form.cleaned_data.get('password')
        remember_me = form.cleaned_data.get('remember_me', False)

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
                messages.add_message(self.request, messages.ERROR, "Your account is not active yet.")
                return HttpResponseRedirect(self.error_url)
            else:
                if not remember_me:
                    self.request.session.set_expiry(0)
                login(self.request, user)
        else:
            return self.form_invalid(form)

        return HttpResponseRedirect(reverse_lazy('profile:index', args=[user.username]))

    def form_invalid(self, form):
        """
        Set an error message if the form is invalid.
        """
        print form.data
        messages.add_message(self.request, messages.ERROR, self.error_msg)
        return HttpResponseRedirect(self.error_url)


class SignUpFormView(generic.FormView):
    template_name = "profile/signup.html"
    form_class = SignUpModelForm
    success_url = reverse_lazy('index')
    error_url = reverse_lazy('index')
    error_msg = "The signup process failed. Please try again."
    form_prefix = "signup"

    def render_to_response(self, context, **response_kwargs):
        """
        Ensure only ajax requests are allowed to render this view.
        """
        if self.request.is_ajax():
            return super(SignUpFormView, self).render_to_response(context, **response_kwargs)
        return HttpResponseBadRequest()

    def get_form_kwargs(self):
        kwargs = super(generic.FormView, self).get_form_kwargs()
        if self.form_prefix:
            kwargs.update({'prefix': self.form_prefix})
        return kwargs

    def form_valid(self, form):
        """
        Set a success message if the form is valid.
        """
        user = form.save()
        user.is_active = False
        user.set_password(form.cleaned_data.get('password'))
        user.save()

        if user:
            user.profile.add_notification('activate_profile')
            messages.add_message(
                self.request, messages.SUCCESS,
                "Thank you for signing up. An email has been sent to you with a link to activate your profile."
            )
            return HttpResponseRedirect(self.success_url)
            return self.form_invalid(form)
        return self.form_invalid(form)

    def form_invalid(self, form):
        """
        Set an error message if the form is invalid.
        """
        messages.add_message(self.request, messages.ERROR, self.error_msg)
        return HttpResponseRedirect(self.error_url)


class UpdateFormView(generic.FormView):
    template_name = "profile/update.html"
    form_class = UpdateModelForm
    success_url = reverse_lazy('index')
    error_url = reverse_lazy('index')
    error_msg = "Updating your profile failed. Please try again."
    form_prefix = "update"

    def render_to_response(self, context, **response_kwargs):
        """
        Ensure only ajax requests are allowed to render this view.
        """
        if self.request.is_ajax():
            return super(UpdateFormView, self).render_to_response(context, **response_kwargs)
        return HttpResponseBadRequest()

    def get_form_kwargs(self):
        kwargs = super(generic.FormView, self).get_form_kwargs()
        if self.form_prefix:
            kwargs.update({'prefix': self.form_prefix})
        if hasattr(self.request.user, 'profile'):
            kwargs.update({'instance': self.request.user.profile})
        return kwargs

    def get_initial(self):
        try:
            return self.request.user.profile.__dict__
        except AttributeError:
            return {}

    def form_valid(self, form):
        """
        Set a success message if the form is valid.
        """
        if form.is_valid():
            form.save()
            messages.add_message(
                self.request, messages.SUCCESS,
                "Your profile hase been successfully updated."
            )
            return HttpResponseRedirect(self.success_url)

        return self.form_invalid(form)

    def form_invalid(self, form):
        """
        Set an error message if the form is invalid.
        """
        messages.add_message(self.request, messages.ERROR, self.error_msg)
        return HttpResponseRedirect(self.error_url)


class ResetPasswordFormView(generic.FormView):
    template_name = "profile/reset_password.html"
    form_class = ResetPasswordForm
    success_url = reverse_lazy('index')
    error_url = reverse_lazy('index')
    error_msg = "Password reset failed."
    form_prefix = "reset_password"

    def render_to_response(self, context, **response_kwargs):
        """
        Ensure only ajax requests are allowed to render this view.
        """
        if self.request.is_ajax():
            return super(ResetPasswordFormView, self).render_to_response(context, **response_kwargs)
        return HttpResponseBadRequest()

    def get_form_kwargs(self):
        kwargs = super(generic.FormView, self).get_form_kwargs()
        if self.form_prefix:
            kwargs.update({'prefix': self.form_prefix})
        return kwargs

    def form_valid(self, form):
        """
        Set a success message if the form is valid.
        """
        user = User.objects.get(email=form.cleaned_data.get('email'))

        if user:
            user.profile.add_notification('reset_password')
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


class ResendActivationFormView(generic.FormView):
    template_name = "profile/resend_activation.html"
    form_class = ResendActivationForm
    success_url = reverse_lazy('index')
    error_url = reverse_lazy('index')
    error_msg = "Activation email resend failed."
    form_prefix = "resend_activation"

    def render_to_response(self, context, **response_kwargs):
        """
        Ensure only ajax requests are allowed to render this view.
        """
        if self.request.is_ajax():
            return super(ResendActivationFormView, self).render_to_response(context, **response_kwargs)
        return HttpResponseBadRequest()

    def get_form_kwargs(self):
        kwargs = super(generic.FormView, self).get_form_kwargs()
        if self.form_prefix:
            kwargs.update({'prefix': self.form_prefix})
        return kwargs

    def form_valid(self, form):
        """
        Set a success message if the form is valid.
        """
        user = User.objects.get(email=form.cleaned_data.get('email'))

        if user:
            user.profile.add_notification('activate_profile')
            messages.add_message(
                self.request, messages.SUCCESS,
                "An email has been sent to you with a link to activate your profile."
            )
            return HttpResponseRedirect(self.success_url)
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
        return reverse_lazy('index')


class ValidateView(generic.View):

    @json_response
    def get(self, request, type, *args, **kwargs):
        username = None
        email = None

        auth_username = getattr(self.request.user, 'username', None)
        auth_email = getattr(self.request.user, 'email', None)

        for key in request.GET.keys():
            if "username" in key:
                username = request.GET.get(key)
                if username == auth_username:
                    return True if type == 'unique' else False

            elif "email" in key:
                email = request.GET.get(key)
                if email == auth_email:
                    return True if type == 'unique' else False

        try:
            if username:
                User.objects.get(username=username)
            elif email:
                User.objects.get(email=email)
        except User.DoesNotExist:
            return True if type == 'unique' else False

        return False if type == 'unique' else True


class AssociateRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self):
        self.request.session['show_update'] = True
        return reverse_lazy('index')


class InactiveRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self):
        messages.add_message(
            self.request, messages.ERROR, "Profile has not yet been activated or was deactivated by an administrator."
        )
        return reverse_lazy('index')

index = IndexDetailView.as_view()
signin = SignInFormView.as_view()
signup = SignUpFormView.as_view()
update = UpdateFormView.as_view()
reset_password = ResetPasswordFormView.as_view()
resend_activation = ResendActivationFormView.as_view()
signout = SignOutRedirectView.as_view()
validate = ValidateView.as_view()
associate = AssociateRedirectView.as_view()
inactive = InactiveRedirectView.as_view()