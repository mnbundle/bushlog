from django import forms
from django.core.mail import send_mail

from bushlog import widgets
from bushlog.apps.profile.models import User
from bushlog.utils import choices


class SupportForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'span12 required', 'placeholder': 'Full name'})
    )
    email = forms.EmailField(
        widget=widgets.EmailInput(attrs={'class': 'span12 required email', 'placeholder': 'Email address'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'span12 required', 'placeholder': 'Description of the issue.', 'rows': 4})
    )

    def send(self, *args, **kwargs):
        """
        Sends a notification to support of the issue.
        """
        from_email = "%s <%s>" % (self.cleaned_data.get('full_name', ''), self.cleaned_data.get('email', ''))
        to_email = "Bushlog Support <support@bushlog.com>"

        # send the mail
        return send_mail("Issue Report", self.cleaned_data.get('description'), from_email, [to_email])
