from django import forms
from django.core.urlresolvers import reverse_lazy

from bushlog.apps.location.models import Country
from bushlog.apps.profile.models import UserProfile, User
from bushlog.utils import choices


class SignInForm(forms.Form):
    username_email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'span3', 'placeholder': 'Username / Email address'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'span3', 'placeholder': 'Password'})
    )
    remember_me = forms.BooleanField(required=False)


class SignUpModelForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'span4', 'equalTo': '#id_signup-password'})
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'span4 required', 'minlength': 4, 'remote': reverse_lazy('profile:validate', args=['unique'])}
            ),
            'email': forms.TextInput(
                attrs={'class': 'span4 required email', 'remote': reverse_lazy('profile:validate', args=['unique'])}
            ),
            'password': forms.PasswordInput(attrs={'class': 'span4 required', 'minlength': 6}),
        }

    def clean(self):
        cleaned_data = super(SignUpModelForm, self).clean()
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError("Passwords don't match.")

        return cleaned_data


class UpdateModelForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'span2', 'placeholder': 'First name'}), max_length=30, required=False
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'span2', 'placeholder': 'Last name'}), max_length=30, required=False
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'class': 'span4 required email', 'remote': reverse_lazy('profile:validate', args=['unique'])}
        ),
        required=True
    )

    class Meta:
        model = UserProfile
        fields = ['biography', 'gender', 'birth_date', 'country']
        widgets = {
            'biography': forms.Textarea(attrs={'class': 'span4', 'rows': 5, 'maxlength': 250}),
            'gender': forms.Select(attrs={'class': 'span4'}, choices=choices(['Male', 'Female'])),
            'birth_date': forms.DateInput(attrs={'readonly': 'readonly'}, format='%d/%m/%Y'),
            'country': forms.Select(
                attrs={'class': 'span4'}, choices=tuple([(obj.id, obj.name) for obj in Country.objects.all()])
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UpdateModelForm, self).__init__(*args, **kwargs)

        # initialise the user fields with instance data
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email

    def save(self, *args, **kwargs):
        super(UpdateModelForm, self).save(*args, **kwargs)

        # save the extra user data
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.email = self.cleaned_data.get('email')
        self.instance.user.save()


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'class': 'span4 required email', 'remote': reverse_lazy('profile:validate', args=['exists'])}
        ),
        required=True
    )
