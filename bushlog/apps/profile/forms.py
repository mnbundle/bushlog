from django import forms
from django.contrib.auth.models import User


class SignInForm(forms.Form):
    username_email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'span3', 'placeholder': 'Username / Email address'}), required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'span3', 'placeholder': 'Password'})
    )
    remember_me = forms.BooleanField(required=False)


class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'span4 required', 'minlength': 6}), required=True
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'span4 required', 'minlength': 4}),
            'email': forms.TextInput(attrs={'class': 'span4 required email'}),
            'password': forms.PasswordInput(attrs={'class': 'span4 required', 'minlength': 6}),
        }

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        if cleaned_data['password'] != cleaned_data['password']:
            raise forms.ValidationError("Your password does not match the confirmed password.")

        return cleaned_data
