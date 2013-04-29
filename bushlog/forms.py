from django import forms
from django.core.mail import mail_admins

from bushlog import widgets


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
        mail_admins(
            "Support Issue", "%s (%s) has reported an issue.\n\r %s" % (
                self.cleaned_data.get('full_name'), self.cleaned_data.get('email'), self.cleaned_data.get('description')
            )
        )

